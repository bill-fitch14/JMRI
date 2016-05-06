// AddSignalMastPanel.java
package jmri.jmrit.beantable.signalmast;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.io.File;
import java.net.URISyntaxException;
import java.net.URL;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSpinner;
import javax.swing.SpinnerNumberModel;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;
import jmri.InstanceManager;
import jmri.NamedBean;
import jmri.NmraPacket;
import jmri.SignalAppearanceMap;
import jmri.SignalHead;
import jmri.SignalMast;
import jmri.SignalSystem;
import jmri.SignalSystemManager;
import jmri.Turnout;
import jmri.implementation.DccSignalMast;
import jmri.implementation.SignalHeadSignalMast;
import jmri.implementation.TurnoutSignalMast;
import jmri.implementation.VirtualSignalMast;
import jmri.implementation.MatrixSignalMast;
import jmri.util.ConnectionNameFromSystemName;
import jmri.util.FileUtil;
import jmri.util.StringUtil;
import jmri.util.swing.BeanSelectCreatePanel;
import jmri.util.swing.JmriBeanComboBox;
import org.jdom2.Element;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * JPanel to create a new SignalMast
 *
 * @author	Bob Jacobsen Copyright (C) 2009, 2010
 * @version $Revision$
 */
public class AddSignalMastPanel extends JPanel {

    private static final long serialVersionUID = 2027577182244302143L;
    jmri.UserPreferencesManager prefs = jmri.InstanceManager.getDefault(jmri.UserPreferencesManager.class);
    String systemSelectionCombo = this.getClass().getName() + ".SignallingSystemSelected";
    String mastSelectionCombo = this.getClass().getName() + ".SignallingMastSelected";
    String driverSelectionCombo = this.getClass().getName() + ".SignallingDriverSelected";
    List<NamedBean> alreadyUsed = new ArrayList<NamedBean>();

    JComboBox<String> signalMastDriver;

    JPanel signalHeadPanel = new JPanel();
    JPanel turnoutMastPanel = new JPanel();
    JScrollPane turnoutMastScroll;
    JScrollPane dccMastScroll;
    JPanel dccMastPanel = new JPanel();
    JLabel systemPrefixBoxLabel = new JLabel(Bundle.getMessage("DCCSystem") + ":");
    JComboBox<String> systemPrefixBox = new JComboBox<String>();
    JLabel dccAspectAddressLabel = new JLabel(Bundle.getMessage("DCCMastAddress"));
    JTextField dccAspectAddressField = new JTextField(5);
    JCheckBox allowUnLit = new JCheckBox();
    JPanel unLitSettingsPanel = new JPanel();
    JScrollPane matrixMastScroll;
    JPanel matrixMastPanel = new JPanel();
    JSpinner bitNumSpinner = new JSpinner();

    JButton cancel = new JButton(Bundle.getMessage("ButtonCancel"));

    SignalMast mast = null;

    public AddSignalMastPanel() {

        signalMastDriver = new JComboBox<String>(new String[]{
            Bundle.getMessage("HeadCtlMast"), Bundle.getMessage("TurnCtlMast"), Bundle.getMessage("VirtualMast"), Bundle.getMessage("MatrixCtlMast")
        });
        //Only allow the creation of DCC SignalMast if a command station instance is present, otherwise it will not work, so no point in adding it.
        if (jmri.InstanceManager.getList(jmri.CommandStation.class) != null) {
            signalMastDriver.addItem(Bundle.getMessage("DCCMast"));
            java.util.List<jmri.CommandStation> connList = jmri.InstanceManager.getList(jmri.CommandStation.class);
            for (int x = 0; x < connList.size(); x++) {
                if (connList.get(x) instanceof jmri.jmrix.loconet.SlotManager) {
                    signalMastDriver.addItem(Bundle.getMessage("LNCPMast"));
                    break;
                }
            }
        }

        refreshHeadComboBox();
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));

        JPanel p;
        p = new JPanel();
        p.setLayout(new jmri.util.javaworld.GridLayout2(5, 2));

        JLabel l = new JLabel(Bundle.getMessage("LabelUserName"));
        p.add(l);
        p.add(userName);

        l = new JLabel(Bundle.getMessage("SigSys") + ": ");
        p.add(l);
        p.add(sigSysBox);

        l = new JLabel(Bundle.getMessage("MastType") + ": ");
        p.add(l);
        p.add(mastBox);

        l = new JLabel(Bundle.getMessage("DriverType") + ": ");
        p.add(l);
        p.add(signalMastDriver);

        l = new JLabel(Bundle.getMessage("AllowUnLitLabel"));
        p.add(l);
        p.add(allowUnLit);

        add(p);

        unLitSettingsPanel.add(dccUnLitPanel);
        unLitSettingsPanel.add(turnoutUnLitPanel);
        unLitSettingsPanel.add(matrixUnLitPanel);
        turnoutUnLitPanel();
        dccUnLitPanel();
        matrixUnLitPanel();

        add(unLitSettingsPanel);

        TitledBorder border = BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.black));
        border.setTitle(Bundle.getMessage("MenuItemSignalTable")); // Signal Heads
        signalHeadPanel.setBorder(border);
        signalHeadPanel.setVisible(false);
        add(signalHeadPanel);

        TitledBorder disableborder = BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.black));
        disableborder.setTitle("Disable specific Aspects"); //I18N ToDo
        disabledAspectsScroll = new JScrollPane(disabledAspectsPanel);
        disabledAspectsScroll.setBorder(disableborder);
        disabledAspectsScroll.setVisible(false);
        add(disabledAspectsScroll);

        turnoutMastScroll = new JScrollPane(turnoutMastPanel);
        turnoutMastScroll.setBorder(BorderFactory.createEmptyBorder());
        turnoutMastScroll.setVisible(false);
        add(turnoutMastScroll);

        dccMastScroll = new JScrollPane(dccMastPanel);
        dccMastScroll.setBorder(BorderFactory.createEmptyBorder());
        dccMastScroll.setVisible(false);
        add(dccMastScroll);

        matrixMastScroll = new JScrollPane(matrixMastPanel); // EBR
        matrixMastScroll.setBorder(BorderFactory.createEmptyBorder());
        matrixMastScroll.setVisible(false);
        JLabel turnoutStateLabel = new JLabel(Bundle.getMessage("SetState"));
        // added in getPanel (turnout & aspect)
        JComboBox<String> turnoutState = new JComboBox<String>(turnoutStates);
        add(matrixMastScroll);

        JButton ok;
        JPanel buttonHolder = new JPanel();
        cancel.setVisible(false);
        buttonHolder.add(cancel);
        buttonHolder.add(ok = new JButton(Bundle.getMessage("ButtonOK")));
        ok.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                okPressed(e);
            }
        });

        add(buttonHolder);

        if (prefs.getComboBoxLastSelection(driverSelectionCombo) != null) {
            signalMastDriver.setSelectedItem(prefs.getComboBoxLastSelection(driverSelectionCombo));
        }

        signalMastDriver.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                updateSelectedDriver();
            }
        });

        allowUnLit.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                updateUnLit();
            }
        });

        includeUsed.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                refreshHeadComboBox();
            }
        });

        // load the list of signal systems
        SignalSystemManager man = InstanceManager.signalSystemManagerInstance();
        String[] names = man.getSystemNameArray();
        for (int i = 0; i < names.length; i++) {
            sigSysBox.addItem(man.getSystem(names[i]).getUserName());
        }
        if (prefs.getComboBoxLastSelection(systemSelectionCombo) != null) {
            sigSysBox.setSelectedItem(prefs.getComboBoxLastSelection(systemSelectionCombo));
        }

        loadMastDefinitions();
        updateSelectedDriver();
        updateHeads();
        refreshHeadComboBox();
        sigSysBox.addItemListener(new ItemListener() {
            public void itemStateChanged(ItemEvent e) {
                loadMastDefinitions();
                updateSelectedDriver();
            }
        });
    }

    boolean inEditMode = false;

    public AddSignalMastPanel(SignalMast mast) {
        this();
        inEditMode = true;
        this.mast = mast;
        sigSysBox.setEnabled(false);
        mastBox.setEnabled(false);
        signalMastDriver.setEnabled(false);
        userName.setText(mast.getUserName());
        userName.setEnabled(false);
        sigSysBox.setSelectedItem(mast.getSignalSystem().getUserName());
        loadMastDefinitions();
        allowUnLit.setSelected(mast.allowUnLit());
        String mastType = "appearance-" + extractMastTypeFromMast(((jmri.implementation.AbstractSignalMast) mast).getSystemName()) + ".xml";
        for (int i = 0; i < mastNames.size(); i++) {
            if (mastNames.get(i).getName().endsWith(mastType)) {
                mastBox.setSelectedIndex(i);
                break;
            }
        }
        mastNames.get(mastBox.getSelectedIndex()).getName();

        signalMastDriver.setEnabled(false);

        systemPrefixBoxLabel.setEnabled(true);
        systemPrefixBox.setEnabled(true);
        dccAspectAddressLabel.setEnabled(true);
        dccAspectAddressField.setEnabled(true);

        if (mast instanceof jmri.implementation.SignalHeadSignalMast) {
            signalMastDriver.setSelectedItem(Bundle.getMessage("HeadCtlMast"));
            updateSelectedDriver();

            signalHeadPanel.setVisible(false);

            List<String> disabled = ((SignalHeadSignalMast) mast).getDisabledAspects();
            if (disabled != null) {
                for (String aspect : disabled) {
                    if (disabledAspects.containsKey(aspect)) {
                        disabledAspects.get(aspect).setSelected(true);
                    }
                }
            }
        } else if (mast instanceof jmri.implementation.TurnoutSignalMast) {
            signalMastDriver.setSelectedItem(Bundle.getMessage("TurnCtlMast"));
            updateSelectedDriver();
            SignalAppearanceMap appMap = mast.getAppearanceMap();
            TurnoutSignalMast tmast = (TurnoutSignalMast) mast;

            if (appMap != null) {
                java.util.Enumeration<String> aspects = appMap.getAspects();
                while (aspects.hasMoreElements()) {
                    String key = aspects.nextElement();
                    TurnoutAspectPanel turnPanel = turnoutAspect.get(key);
                    turnPanel.setSelectedTurnout(tmast.getTurnoutName(key));
                    turnPanel.setTurnoutState(tmast.getTurnoutState(key));
                    turnPanel.setAspectDisabled(tmast.isAspectDisabled(key));
                }
            }
            if (tmast.resetPreviousStates()) {
                resetPreviousState.setSelected(true);
            }
            if (tmast.allowUnLit()) {
                turnoutUnLitBox.setDefaultNamedBean(tmast.getUnLitTurnout());
                if (tmast.getUnLitTurnoutState() == Turnout.CLOSED) {
                    turnoutUnLitState.setSelectedItem(stateClosed);
                } else {
                    turnoutUnLitState.setSelectedItem(stateThrown);
                }

            }
        } else if (mast instanceof jmri.implementation.VirtualSignalMast) {
            signalMastDriver.setSelectedItem(Bundle.getMessage("VirtualMast"));
            updateSelectedDriver();
            List<String> disabled = ((VirtualSignalMast) mast).getDisabledAspects();
            if (disabled != null) {
                for (String aspect : disabled) {
                    if (disabledAspects.containsKey(aspect)) {
                        disabledAspects.get(aspect).setSelected(true);
                    }
                }
            }
        } else if (mast instanceof jmri.implementation.DccSignalMast) {
            if (mast instanceof jmri.jmrix.loconet.LNCPSignalMast) {
                signalMastDriver.setSelectedItem(Bundle.getMessage("LNCPMast"));
            } else {
                signalMastDriver.setSelectedItem(Bundle.getMessage("DCCMast"));
            }

            updateSelectedDriver();
            SignalAppearanceMap appMap = mast.getAppearanceMap();
            DccSignalMast dmast = (DccSignalMast) mast;

            if (appMap != null) {
                java.util.Enumeration<String> aspects = appMap.getAspects();
                while (aspects.hasMoreElements()) {
                    String key = aspects.nextElement();
                    DCCAspectPanel dccPanel = dccAspect.get(key);
                    dccPanel.setAspectDisabled(dmast.isAspectDisabled(key));
                    if (!dmast.isAspectDisabled(key)) {
                        dccPanel.setAspectId(dmast.getOutputForAppearance(key));
                    }

                }
            }
            java.util.List<jmri.CommandStation> connList = jmri.InstanceManager.getList(jmri.CommandStation.class);
            if (connList != null) {
                for (int x = 0; x < connList.size(); x++) {
                    jmri.CommandStation station = connList.get(x);
                    systemPrefixBox.addItem(station.getUserName());
                }
            } else {
                systemPrefixBox.addItem("None");
            }
            dccAspectAddressField.setText("" + dmast.getDccSignalMastAddress());
            systemPrefixBox.setSelectedItem(dmast.getCommandStation().getUserName());

            systemPrefixBoxLabel.setEnabled(false);
            systemPrefixBox.setEnabled(false);
            dccAspectAddressLabel.setEnabled(false);
            dccAspectAddressField.setEnabled(false);
            if (dmast.allowUnLit()) {
                unLitAspectField.setText("" + dmast.getUnlitId());
            }
        } else if (mast instanceof jmri.implementation.MatrixSignalMast) { // EBR, copied from DCC Mast
            signalMastDriver.setSelectedItem(Bundle.getMessage("MatrixCtlMast"));
            updateSelectedDriver();
            SignalAppearanceMap appMap = mast.getAppearanceMap();
            MatrixSignalMast xmast = (MatrixSignalMast) mast;

            if (appMap != null) {
                java.util.Enumeration<String> aspects = appMap.getAspects();
                while (aspects.hasMoreElements()) {
                    String key = aspects.nextElement();
                    // select the right checkboxes ToDo
                    MatrixAspectPanel matrixPanel = matrixAspect.get(key);
                    //matrixPanel.setSelectedTurnout(xmast.getTurnoutName(key));
                    //matrixPanel.setTurnoutState(xmast.getTurnoutState(key));
                    matrixPanel.setAspectDisabled(xmast.isAspectDisabled(key));
                }
            }
            if (xmast.resetPreviousStates()) {
                resetPreviousState.setSelected(true);
            }
            if (xmast.allowUnLit()) {
                turnoutUnLitBox.setDefaultNamedBean(xmast.getUnLitTurnout());
                if (xmast.getUnLitTurnoutState() == Turnout.CLOSED) {
                    turnoutUnLitState.setSelectedItem(stateClosed);
                } else {
                    turnoutUnLitState.setSelectedItem(stateThrown);
                }
            }
        }
        cancel.setVisible(true);
        cancel.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                ((jmri.util.JmriJFrame) getTopLevelAncestor()).dispose();
            }
        });
    }

    String extractMastTypeFromMast(String name) {
        String[] parts = name.split(":");
        if (parts.length > 3) {
            // See if old format, new format uses () around the signal head names
            return(parts[2]);
        }
        return parts[2].substring(0, parts[2].indexOf("("));
    }

    protected void updateSelectedDriver() {
        signalHeadPanel.setVisible(false);
        turnoutMastScroll.setVisible(false);
        disabledAspectsScroll.setVisible(false);
        dccMastScroll.setVisible(false);
        matrixMastScroll.setVisible(false);
        if (Bundle.getMessage("TurnCtlMast").equals(signalMastDriver.getSelectedItem())) {
            updateTurnoutAspectPanel();
            turnoutMastScroll.setVisible(true);
        } else if (Bundle.getMessage("HeadCtlMast").equals(signalMastDriver.getSelectedItem())) {
            updateHeads();
            updateDisabledOption();
            signalHeadPanel.setVisible(true);
            disabledAspectsScroll.setVisible(true);
        } else if (Bundle.getMessage("VirtualMast").equals(signalMastDriver.getSelectedItem())) {
            updateDisabledOption();
            disabledAspectsScroll.setVisible(true);
        } else if ((Bundle.getMessage("DCCMast").equals(signalMastDriver.getSelectedItem())) || (Bundle.getMessage("LNCPMast").equals(signalMastDriver.getSelectedItem()))) {
            updateDCCMastPanel();
            dccMastScroll.setVisible(true);
        } else if (Bundle.getMessage("MatrixMast").equals(signalMastDriver.getSelectedItem())) { // EBR
            updateMatrixAspectPanel();
            matrixMastScroll.setVisible(true);
        }
        updateUnLit();
        validate();
        if (getTopLevelAncestor() != null) {
            ((jmri.util.JmriJFrame) getTopLevelAncestor()).setSize(((jmri.util.JmriJFrame) getTopLevelAncestor()).getPreferredSize());
            ((jmri.util.JmriJFrame) getTopLevelAncestor()).pack();
        }
        repaint();
    }

    protected void updateUnLit() {
        dccUnLitPanel.setVisible(false);
        turnoutUnLitPanel.setVisible(false);
        matrixUnLitPanel.setVisible(false);
        if (allowUnLit.isSelected()) {
            if (Bundle.getMessage("TurnCtlMast").equals(signalMastDriver.getSelectedItem())) {
                turnoutUnLitPanel.setVisible(true);
            } else if ((Bundle.getMessage("DCCMast").equals(signalMastDriver.getSelectedItem())) || (Bundle.getMessage("LNCPMast").equals(signalMastDriver.getSelectedItem())) ) {
                dccUnLitPanel.setVisible(true);
            } else if (Bundle.getMessage("MatrixCtlMast").equals(signalMastDriver.getSelectedItem())) {
                matrixUnLitPanel.setVisible(true);
            }
        }
        validate();
        if (getTopLevelAncestor() != null) {
            ((jmri.util.JmriJFrame) getTopLevelAncestor()).setSize(((jmri.util.JmriJFrame) getTopLevelAncestor()).getPreferredSize());
            ((jmri.util.JmriJFrame) getTopLevelAncestor()).pack();
        }
        repaint();
    }

    JTextField userName = new JTextField(20);
    JComboBox<String> sigSysBox = new JComboBox<String>();
    JComboBox<String> mastBox = new JComboBox<String>(new String[]{Bundle.getMessage("MastEmpty")});
    JCheckBox includeUsed = new JCheckBox(Bundle.getMessage("IncludeUsedHeads"));
    JCheckBox resetPreviousState = new JCheckBox(Bundle.getMessage("ResetPrevious"));

    String sigsysname;
    ArrayList<File> mastNames = new ArrayList<File>();

    HashMap<String, JCheckBox> disabledAspects = new HashMap<String, JCheckBox>(10);
    JPanel disabledAspectsPanel = new JPanel();
    JScrollPane disabledAspectsScroll;

    void updateDisabledOption() {
        String mastType = mastNames.get(mastBox.getSelectedIndex()).getName();
        mastType = mastType.substring(11, mastType.indexOf(".xml"));
        jmri.implementation.DefaultSignalAppearanceMap sigMap = jmri.implementation.DefaultSignalAppearanceMap.getMap(sigsysname, mastType);
        java.util.Enumeration<String> aspects = sigMap.getAspects();
        disabledAspects = new HashMap<String, JCheckBox>(5);

        while (aspects.hasMoreElements()) {
            String aspect = aspects.nextElement();
            JCheckBox disabled = new JCheckBox(aspect);
            disabledAspects.put(aspect, disabled);
        }
        disabledAspectsPanel.removeAll();
        disabledAspectsPanel.setLayout(new jmri.util.javaworld.GridLayout2(disabledAspects.size() + 1, 1));
        for (String aspect : disabledAspects.keySet()) {
            disabledAspectsPanel.add(disabledAspects.get(aspect));
        }
    }

    void loadMastDefinitions() {
        // need to remove itemListener before addItem() or item event will occur
        if (mastBox.getItemListeners().length > 0) { // should this be a while loop?
            mastBox.removeItemListener(mastBox.getItemListeners()[0]);
        }
        mastBox.removeAllItems();
        try {
            mastNames = new ArrayList<File>();
            SignalSystemManager man = InstanceManager.signalSystemManagerInstance();

            // get the signals system name from the user name in combo box
            String u = (String) sigSysBox.getSelectedItem();
            sigsysname = man.getByUserName(u).getSystemName();
            map = new HashMap<String, Integer>();

            // do file IO to get all the appearances
            // gather all the appearance files
            //Look for the default system defined ones first
            URL path = FileUtil.findURL("xml/signals/" + sigsysname, FileUtil.Location.INSTALLED);
            if (path != null) {
                File[] apps = new File(path.toURI()).listFiles();
                for (File app : apps) {
                    if (app.getName().startsWith("appearance") && app.getName().endsWith(".xml")) {
                        log.debug("   found file: " + app.getName());
                        // load it and get name
                        mastNames.add(app);
                        jmri.jmrit.XmlFile xf = new jmri.jmrit.XmlFile() {
                        };
                        Element root = xf.rootFromFile(app);
                        String name = root.getChild("name").getText();
                        mastBox.addItem(name);
                        map.put(name, root.getChild("appearances")
                                .getChild("appearance")
                                .getChildren("show")
                                .size());
                    }
                }
            }
        } catch (org.jdom2.JDOMException e) {
            mastBox.addItem("Failed to create definition, did you select a system?");
            log.warn("in loadMastDefinitions", e);
        } catch (java.io.IOException | URISyntaxException e) {
            mastBox.addItem("Failed to read definition, did you select a system?");
            log.warn("in loadMastDefinitions", e);
        }

        try {
            URL path = FileUtil.findURL("signals/" + sigsysname, FileUtil.Location.USER, "xml", "resources");
            if (path != null) {
                File[] apps = new File(path.toURI()).listFiles();
                for (File app : apps) {
                    if (app.getName().startsWith("appearance") && app.getName().endsWith(".xml")) {
                        log.debug("   found file: " + app.getName());
                        // load it and get name 
                        // If the mast file name already exists no point in re-adding it
                        if (!mastNames.contains(app)) {
                            mastNames.add(app);
                            jmri.jmrit.XmlFile xf = new jmri.jmrit.XmlFile() {
                            };
                            Element root = xf.rootFromFile(app);
                            String name = root.getChild("name").getText();
                            //if the mast name already exist no point in readding it.
                            if (!map.containsKey(name)) {
                                mastBox.addItem(name);
                                map.put(name, root.getChild("appearances")
                                        .getChild("appearance")
                                        .getChildren("show")
                                        .size());
                            }
                        }
                    }
                }
            }
        } catch (org.jdom2.JDOMException | java.io.IOException | URISyntaxException e) {
            log.warn("in loadMastDefinitions", e);
        }
        mastBox.addItemListener(new ItemListener() {
            public void itemStateChanged(ItemEvent e) {
                updateSelectedDriver();
            }
        });
        updateSelectedDriver();

        if (prefs.getComboBoxLastSelection(mastSelectionCombo + ":" + ((String) sigSysBox.getSelectedItem())) != null) {
            mastBox.setSelectedItem(prefs.getComboBoxLastSelection(mastSelectionCombo + ":" + ((String) sigSysBox.getSelectedItem())));
        }

    }

    HashMap<String, Integer> map = new HashMap<String, Integer>();

    void updateHeads() {
        if (!Bundle.getMessage("HeadCtlMast").equals(signalMastDriver.getSelectedItem())) {
            return;
        }
        if (mastBox.getSelectedItem() == null) {
            return;
        }
        int count = map.get(mastBox.getSelectedItem()).intValue();
        headList = new ArrayList<JmriBeanComboBox>(count);
        signalHeadPanel.removeAll();
        signalHeadPanel.setLayout(new jmri.util.javaworld.GridLayout2(count + 1, 1));
        for (int i = 0; i < count; i++) {
            JmriBeanComboBox head = new JmriBeanComboBox(InstanceManager.signalHeadManagerInstance());
            head.excludeItems(alreadyUsed);
            headList.add(head);
            signalHeadPanel.add(head);
        }
        signalHeadPanel.add(includeUsed);
    }

    void okPressed(ActionEvent e) {
        String mastname = mastNames.get(mastBox.getSelectedIndex()).getName();

        String user = userName.getText().trim();
        if (user.equals("")) {
            int i = JOptionPane.showConfirmDialog(null, "No Username has been defined, this may cause issues when editing the mast later.\nAre you sure that you want to continue?",
                    "No UserName Given",
                    JOptionPane.YES_NO_OPTION);
            if (i != 0) {
                return;
            }
        }
        if (mast == null) {
            if (!checkUserName(userName.getText())) {
                return;
            }
            if (Bundle.getMessage("HeadCtlMast").equals(signalMastDriver.getSelectedItem())) {
                if (!checkSignalHeadUse()) {
                    return;
                }
                StringBuilder build = new StringBuilder();
                build.append("IF$shsm:"
                        + sigsysname
                        + ":" + mastname.substring(11, mastname.length() - 4));
                for (JmriBeanComboBox head : headList) {
                    build.append("(" + StringUtil.parenQuote(head.getSelectedDisplayName()) + ")");
                }
                String name = build.toString();
                log.debug("add signal: " + name);
                SignalMast m = InstanceManager.signalMastManagerInstance().getSignalMast(name);
                if (m != null) {
                    JOptionPane.showMessageDialog(null, java.text.MessageFormat.format(Bundle.getMessage("DuplicateMast"),
                            new Object[]{m.getDisplayName()}), Bundle.getMessage("DuplicateMastTitle"), JOptionPane.INFORMATION_MESSAGE);
                    return;
                }
                try {
                    m = InstanceManager.signalMastManagerInstance().provideSignalMast(name);
                } catch (IllegalArgumentException ex) {
                    // user input no good
                    handleCreateException(name);
                    return; // without creating       
                }
                if (!user.equals("")) {
                    m.setUserName(user);
                }

                for (String aspect : disabledAspects.keySet()) {
                    if (disabledAspects.get(aspect).isSelected()) {
                        ((SignalHeadSignalMast) m).setAspectDisabled(aspect);
                    } else {
                        ((SignalHeadSignalMast) m).setAspectEnabled(aspect);
                    }
                }
                m.setAllowUnLit(allowUnLit.isSelected());
            } else if (Bundle.getMessage("TurnCtlMast").equals(signalMastDriver.getSelectedItem())) {
                String name = "IF$tsm:"
                        + sigsysname
                        + ":" + mastname.substring(11, mastname.length() - 4);
                name += "($" + (paddedNumber.format(TurnoutSignalMast.getLastRef() + 1)) + ")";
                TurnoutSignalMast turnMast = new TurnoutSignalMast(name);
                for (String aspect : turnoutAspect.keySet()) {
                    turnoutAspect.get(aspect).setReference(name + ":" + aspect);
                    turnoutMastPanel.add(turnoutAspect.get(aspect).getPanel());
                    if (turnoutAspect.get(aspect).isAspectDisabled()) {
                        turnMast.setAspectDisabled(aspect);
                    } else {
                        turnMast.setAspectEnabled(aspect);
                        turnMast.setTurnout(aspect, turnoutAspect.get(aspect).getTurnoutName(), turnoutAspect.get(aspect).getTurnoutState());
                    }
                }
                turnMast.resetPreviousStates(resetPreviousState.isSelected());
                if (!user.equals("")) {
                    turnMast.setUserName(user);
                }
                InstanceManager.signalMastManagerInstance().register(turnMast);
                turnMast.setAllowUnLit(allowUnLit.isSelected());
                if (allowUnLit.isSelected()) {
                    turnMast.setUnLitTurnout(turnoutUnLitBox.getDisplayName(), turnoutStateValues[turnoutUnLitState.getSelectedIndex()]);
                }
            } else if (Bundle.getMessage("VirtualMast").equals(signalMastDriver.getSelectedItem())) {
                String name = "IF$vsm:"
                        + sigsysname
                        + ":" + mastname.substring(11, mastname.length() - 4);
                name += "($" + (paddedNumber.format(VirtualSignalMast.getLastRef() + 1)) + ")";
                VirtualSignalMast virtMast = new VirtualSignalMast(name);
                if (!user.equals("")) {
                    virtMast.setUserName(user);
                }
                InstanceManager.signalMastManagerInstance().register(virtMast);

                for (String aspect : disabledAspects.keySet()) {
                    if (disabledAspects.get(aspect).isSelected()) {
                        virtMast.setAspectDisabled(aspect);
                    } else {
                        virtMast.setAspectEnabled(aspect);
                    }
                }
                virtMast.setAllowUnLit(allowUnLit.isSelected());
            } else if ((Bundle.getMessage("DCCMast").equals(signalMastDriver.getSelectedItem())) || (Bundle.getMessage("LNCPMast").equals(signalMastDriver.getSelectedItem()))) {
                if (!validateDCCAddress()) {
                    return;
                }
                String systemNameText = ConnectionNameFromSystemName.getPrefixFromName((String) systemPrefixBox.getSelectedItem());
                //if we return a null string then we will set it to use internal, thus picking up the default command station at a later date.
                if (systemNameText.equals("\0")) {
                    systemNameText = "I";
                }
                if (Bundle.getMessage("LNCPMast").equals(signalMastDriver.getSelectedItem())) {
                    systemNameText = systemNameText + "F$lncpsm:";
                } else {
                    systemNameText = systemNameText + "F$dsm:";
                }
                String name = systemNameText
                        + sigsysname
                        + ":" + mastname.substring(11, mastname.length() - 4);
                name += "(" + dccAspectAddressField.getText() + ")";
                DccSignalMast dccMast;
                if (Bundle.getMessage("LNCPMast").equals(signalMastDriver.getSelectedItem())) {
                    dccMast = new jmri.jmrix.loconet.LNCPSignalMast(name);
                } else {
                    dccMast = new DccSignalMast(name);
                }
                for (String aspect : dccAspect.keySet()) {
                    dccMastPanel.add(dccAspect.get(aspect).getPanel());
                    if (dccAspect.get(aspect).isAspectDisabled()) {
                        dccMast.setAspectDisabled(aspect);
                    } else {
                        dccMast.setAspectEnabled(aspect);
                        dccMast.setOutputForAppearance(aspect, dccAspect.get(aspect).getAspectId());
                    }
                }
                if (!user.equals("")) {
                    dccMast.setUserName(user);
                }
                dccMast.setAllowUnLit(allowUnLit.isSelected());
                if (allowUnLit.isSelected()) {
                    dccMast.setUnlitId(Integer.parseInt(unLitAspectField.getText()));
                }
                InstanceManager.signalMastManagerInstance().register(dccMast);
            } else if (Bundle.getMessage("MatrixCtlMast").equals(signalMastDriver.getSelectedItem())) { // EBR OK was pressed, new mast with default props
                String name = "IF$xtm:"
                        + sigsysname
                        + ":" + mastname.substring(11, mastname.length() - 4);
                name += "($" + (paddedNumber.format(MatrixSignalMast.getLastRef() + 1)) + ")";
                MatrixSignalMast matrixMast = new MatrixSignalMast(name);
                for (String aspect : matrixAspect.keySet()) { // make matrix, copy of VirtualMast? store , compare with #834
                    matrixAspect.get(aspect).setReference(name + ":" + aspect);
                    matrixMastPanel.add(matrixAspect.get(aspect).getPanel());
                    if (matrixAspect.get(aspect).isAspectDisabled()) {
                        matrixMast.setAspectDisabled(aspect);
                    } else {
                        matrixMast.setAspectEnabled(aspect);
                        matrixMast.setTurnout(aspect, matrixAspect.get(aspect).getTurnoutName(), matrixAspect.get(aspect).getTurnoutState());
                    }
                }
                matrixMast.resetPreviousStates(resetPreviousState.isSelected());
                if (!user.equals("")) {
                    matrixMast.setUserName(user);
                }
                InstanceManager.signalMastManagerInstance().register(matrixMast);
                matrixMast.setAllowUnLit(allowUnLit.isSelected());
                if (allowUnLit.isSelected()) {
                    matrixMast.setUnLitTurnout(matrixUnLitBox.getDisplayName(), turnoutStateValues[turnoutUnLitState.getSelectedIndex()]);
                }
            }
            prefs.addComboBoxLastSelection(systemSelectionCombo, (String) sigSysBox.getSelectedItem());
            prefs.addComboBoxLastSelection(driverSelectionCombo, (String) signalMastDriver.getSelectedItem());
            prefs.addComboBoxLastSelection(mastSelectionCombo + ":" + ((String) sigSysBox.getSelectedItem()), (String) mastBox.getSelectedItem());
            refreshHeadComboBox();
        } else {
            // mast was already available
            if (Bundle.getMessage("HeadCtlMast").equals(signalMastDriver.getSelectedItem())) {
                SignalHeadSignalMast headMast = (SignalHeadSignalMast) mast;
                for (String aspect : disabledAspects.keySet()) {
                    if (disabledAspects.get(aspect).isSelected()) {
                        headMast.setAspectDisabled(aspect);
                    } else {
                        headMast.setAspectEnabled(aspect);
                    }
                }
                headMast.setAllowUnLit(allowUnLit.isSelected());

            } else if (Bundle.getMessage("TurnCtlMast").equals(signalMastDriver.getSelectedItem())) {
                String name = "IF$tsm:"
                        + sigsysname
                        + ":" + mastname.substring(11, mastname.length() - 4);
                TurnoutSignalMast turnMast = (TurnoutSignalMast) mast;
                for (String aspect : turnoutAspect.keySet()) {
                    turnoutAspect.get(aspect).setReference(name + ":" + aspect);
                    turnMast.setTurnout(aspect, turnoutAspect.get(aspect).getTurnoutName(), turnoutAspect.get(aspect).getTurnoutState());
                    turnoutMastPanel.add(turnoutAspect.get(aspect).getPanel());
                    if (turnoutAspect.get(aspect).isAspectDisabled()) {
                        turnMast.setAspectDisabled(aspect);
                    } else {
                        turnMast.setAspectEnabled(aspect);
                    }
                }
                turnMast.resetPreviousStates(resetPreviousState.isSelected());
                turnMast.setAllowUnLit(allowUnLit.isSelected());
                if (allowUnLit.isSelected()) {
                    turnMast.setUnLitTurnout(turnoutUnLitBox.getDisplayName(), turnoutStateValues[turnoutUnLitState.getSelectedIndex()]);
                }
            } else if (Bundle.getMessage("VirtualMast").equals(signalMastDriver.getSelectedItem())) {
                VirtualSignalMast virtMast = (VirtualSignalMast) mast;
                for (String aspect : disabledAspects.keySet()) {
                    if (disabledAspects.get(aspect).isSelected()) {
                        virtMast.setAspectDisabled(aspect);
                    } else {
                        virtMast.setAspectEnabled(aspect);
                    }
                }
                virtMast.setAllowUnLit(allowUnLit.isSelected());
            } else if ((Bundle.getMessage("DCCMast").equals(signalMastDriver.getSelectedItem())) || (Bundle.getMessage("LNCPMast").equals(signalMastDriver.getSelectedItem()))) {
                DccSignalMast dccMast = (DccSignalMast) mast;
                for (String aspect : dccAspect.keySet()) {
                    dccMastPanel.add(dccAspect.get(aspect).getPanel());
                    if (dccAspect.get(aspect).isAspectDisabled()) {
                        dccMast.setAspectDisabled(aspect);
                    } else {
                        dccMast.setAspectEnabled(aspect);
                        dccMast.setOutputForAppearance(aspect, dccAspect.get(aspect).getAspectId());
                    }
                }
                dccMast.setAllowUnLit(allowUnLit.isSelected());
                if (allowUnLit.isSelected()) {
                    dccMast.setUnlitId(Integer.parseInt(unLitAspectField.getText()));
                }
            } else if (Bundle.getMessage("MatrixCtlMast").equals(signalMastDriver.getSelectedItem())) { // EBR OK was pressed, existing
                String name = "IF$xtm:"
                        + sigsysname
                        + ":" + mastname.substring(11, mastname.length() - 4);
                MatrixSignalMast matrixMast = (MatrixSignalMast) mast;
                for (String aspect : matrixAspect.keySet()) {
                    matrixAspect.get(aspect).setReference(name + ":" + aspect);
                    // remove next line, replace with checkboxes EBR compare with #746
                    matrixMast.setTurnout(aspect, matrixAspect.get(aspect).getTurnoutName(), matrixAspect.get(aspect).getTurnoutState());
                    matrixMastPanel.add(matrixAspect.get(aspect).getPanel());
                    if (matrixAspect.get(aspect).isAspectDisabled()) {
                        matrixMast.setAspectDisabled(aspect);
                    } else {
                        matrixMast.setAspectEnabled(aspect);
                    }
                }
                matrixMast.resetPreviousStates(resetPreviousState.isSelected());
                matrixMast.setAllowUnLit(allowUnLit.isSelected());
                if (allowUnLit.isSelected()) {
                    matrixMast.setUnLitTurnout(turnoutUnLitBox.getDisplayName(), turnoutStateValues[turnoutUnLitState.getSelectedIndex()]);
                }
            }
        }
    }

    DecimalFormat paddedNumber = new DecimalFormat("0000");

    boolean checkUserName(String nam) {
        if (!((nam == null) || (nam.equals("")))) {
            // user name changed, check if new name already exists
            NamedBean nB = InstanceManager.signalMastManagerInstance().getByUserName(nam);
            if (nB != null) {
                log.error("User Name is not unique " + nam);
                String msg = Bundle.getMessage("WarningUserName", new Object[]{("" + nam)});
                JOptionPane.showMessageDialog(null, msg,
                        Bundle.getMessage("WarningTitle"),
                        JOptionPane.ERROR_MESSAGE);
                return false;
            }
            //Check to ensure that the username doesn't exist as a systemname.
            nB = InstanceManager.signalMastManagerInstance().getBySystemName(nam);
            if (nB != null) {
                log.error("User Name is not unique " + nam + " It already exists as a System name");
                String msg = Bundle.getMessage("WarningUserNameAsSystem", new Object[]{("" + nam)});
                JOptionPane.showMessageDialog(null, msg,
                        Bundle.getMessage("WarningTitle"),
                        JOptionPane.ERROR_MESSAGE);
                return false;
            }
        }
        return true;

    }

    boolean checkSystemName(String nam) {
        return false;
    }

    boolean checkSignalHeadUse() {
        for (int i = 0; i < headList.size(); i++) {
            JmriBeanComboBox head = headList.get(i);
            NamedBean h = headList.get(i).getSelectedBean();
            for (int j = i; j < headList.size(); j++) {
                JmriBeanComboBox head2check = headList.get(j);
                if ((head2check != head) && (head2check.getSelectedBean() == h)) {
                    if (!duplicateHeadAssigned(headList.get(i).getSelectedDisplayName())) {
                        return false;
                    }
                }
            }
            if (includeUsed.isSelected()) {
                String isUsed = SignalHeadSignalMast.isHeadUsed((SignalHead) h);
                if ((isUsed != null) && (!headAssignedElseWhere(h.getDisplayName(), isUsed))) {
                    return false;
                }
            }
        }
        return true;
    }

    boolean duplicateHeadAssigned(String head) {
        int i = JOptionPane.showConfirmDialog(null, java.text.MessageFormat.format(Bundle.getMessage("DuplicateHeadAssign"),
                new Object[]{head}),
                Bundle.getMessage("DuplicateHeadAssignTitle"),
                JOptionPane.YES_NO_OPTION);

        if (i == 0) {
            return true;
        }
        return false;
    }

    boolean headAssignedElseWhere(String head, String mast) {
        int i = JOptionPane.showConfirmDialog(null, java.text.MessageFormat.format(Bundle.getMessage("AlreadyAssigned"),
                new Object[]{head, mast}),
                Bundle.getMessage("DuplicateHeadAssignTitle"),
                JOptionPane.YES_NO_OPTION);
        if (i == 0) {
            return true;
        }
        return false;
    }

    protected void refreshHeadComboBox() {
        if (!Bundle.getMessage("HeadCtlMast").equals(signalMastDriver.getSelectedItem())) {
            return;
        }
        if (includeUsed.isSelected()) {
            alreadyUsed = new ArrayList<NamedBean>();
        } else {
            List<SignalHead> alreadyUsedHeads = SignalHeadSignalMast.getSignalHeadsUsed();
            alreadyUsed = new ArrayList<NamedBean>();
            for (SignalHead head : alreadyUsedHeads) {
                alreadyUsed.add(head);
            }
        }

        for (JmriBeanComboBox head : headList) {
            head.excludeItems(alreadyUsed);
        }
    }

    void handleCreateException(String sysName) {
        javax.swing.JOptionPane.showMessageDialog(AddSignalMastPanel.this,
                java.text.MessageFormat.format(
                        Bundle.getMessage("ErrorSignalMastAddFailed"),
                        new Object[]{sysName}),
                Bundle.getMessage("ErrorTitle"),
                javax.swing.JOptionPane.ERROR_MESSAGE);
    }

    void updateTurnoutAspectPanel() {
        if (!Bundle.getMessage("TurnCtlMast").equals(signalMastDriver.getSelectedItem())) {
            return;
        }
        turnoutAspect = new HashMap<String, TurnoutAspectPanel>(10);
        String mastType = mastNames.get(mastBox.getSelectedIndex()).getName();
        mastType = mastType.substring(11, mastType.indexOf(".xml"));
        jmri.implementation.DefaultSignalAppearanceMap sigMap = jmri.implementation.DefaultSignalAppearanceMap.getMap(sigsysname, mastType);
        java.util.Enumeration<String> aspects = sigMap.getAspects();
        while (aspects.hasMoreElements()) {
            String aspect = aspects.nextElement();
            TurnoutAspectPanel aPanel = new TurnoutAspectPanel(aspect);
            turnoutAspect.put(aspect, aPanel);
        }

        turnoutMastPanel.removeAll();
        turnoutMastPanel.setLayout(new jmri.util.javaworld.GridLayout2(turnoutAspect.size() + 1, 2));
        for (String aspect : turnoutAspect.keySet()) {
            turnoutMastPanel.add(turnoutAspect.get(aspect).getPanel());
        }

        turnoutMastPanel.add(resetPreviousState);
        resetPreviousState.setToolTipText(Bundle.getMessage("ResetPreviousToolTip"));
    }

    ArrayList<JmriBeanComboBox> headList = new ArrayList<JmriBeanComboBox>(5);

    JPanel turnoutUnLitPanel = new JPanel();

    String stateThrown = InstanceManager.turnoutManagerInstance().getThrownText();
    String stateClosed = InstanceManager.turnoutManagerInstance().getClosedText();
    String[] turnoutStates = new String[]{stateClosed, stateThrown};
    int[] turnoutStateValues = new int[]{Turnout.CLOSED, Turnout.THROWN};

    BeanSelectCreatePanel turnoutUnLitBox = new BeanSelectCreatePanel(InstanceManager.turnoutManagerInstance(), null);
    JComboBox<String> turnoutUnLitState = new JComboBox<String>(turnoutStates);

    void turnoutUnLitPanel() {
        turnoutUnLitPanel.setLayout(new BoxLayout(turnoutUnLitPanel, BoxLayout.Y_AXIS));
        JPanel turnDetails = new JPanel();
        turnDetails.add(turnoutUnLitBox);
        turnDetails.add(new JLabel(Bundle.getMessage("SetState")));
        turnDetails.add(turnoutUnLitState);
        turnoutUnLitPanel.add(turnDetails);
        TitledBorder border = BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.black));
        border.setTitle(Bundle.getMessage("TurnUnLitDetails"));
        turnoutUnLitPanel.setBorder(border);
    }

    HashMap<String, TurnoutAspectPanel> turnoutAspect = new HashMap<String, TurnoutAspectPanel>(10);

    class TurnoutAspectPanel {

        BeanSelectCreatePanel beanBox = new BeanSelectCreatePanel(InstanceManager.turnoutManagerInstance(), null);
        JCheckBox disabledCheck = new JCheckBox(Bundle.getMessage("DisableAspect"));
        JLabel turnoutStateLabel = new JLabel(Bundle.getMessage("SetState"));
        JComboBox<String> turnoutState = new JComboBox<String>(turnoutStates);

        String aspect = "";

        TurnoutAspectPanel(String aspect) {
            this.aspect = aspect;
        }

        TurnoutAspectPanel(String turnoutName, int state) {
            if (turnoutName == null || turnoutName.equals("")) {
                return;
            }
            beanBox.setDefaultNamedBean(InstanceManager.turnoutManagerInstance().getTurnout(turnoutName));
        }

        void setReference(String reference) {
            beanBox.setReference(reference);
        }

        int getTurnoutState() {
            return turnoutStateValues[turnoutState.getSelectedIndex()];
        }

        void setSelectedTurnout(String name) {
            if (name == null || name.equals("")) {
                return;
            }
            beanBox.setDefaultNamedBean(InstanceManager.turnoutManagerInstance().getTurnout(name));
        }

        void setTurnoutState(int state) {
            if (state == Turnout.CLOSED) {
                turnoutState.setSelectedItem(stateClosed);
            } else {
                turnoutState.setSelectedItem(stateThrown);
            }
        }

        void setAspectDisabled(boolean boo) {
            disabledCheck.setSelected(boo);
            if (boo) {
                beanBox.setEnabled(false);
                turnoutStateLabel.setEnabled(false);
                turnoutState.setEnabled(false);
            } else {
                beanBox.setEnabled(true);
                turnoutStateLabel.setEnabled(true);
                turnoutState.setEnabled(true);
            }
        }

        boolean isAspectDisabled() {
            return disabledCheck.isSelected();
        }

        String getTurnoutName() {
            return beanBox.getDisplayName();
        }

        NamedBean getTurnout() {
            try {
                return beanBox.getNamedBean();
            } catch (jmri.JmriException ex) {
                log.warn("skipping creation of turnout");
                return null;
            }
        }

        JPanel panel;

        JPanel getPanel() {
            if (panel == null) {
                panel = new JPanel();
                panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
                JPanel turnDetails = new JPanel();
                turnDetails.add(beanBox);
                turnDetails.add(turnoutStateLabel);
                turnDetails.add(turnoutState);
                panel.add(turnDetails);
                panel.add(disabledCheck);
                TitledBorder border = BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.black));
                border.setTitle(aspect);
                panel.setBorder(border);

                disabledCheck.addActionListener(new ActionListener() {
                    public void actionPerformed(ActionEvent e) {
                        setAspectDisabled(disabledCheck.isSelected());
                    }
                });

            }
            return panel;
        }

    }

    JPanel dccUnLitPanel = new JPanel();
    JTextField unLitAspectField = new JTextField(5);

    HashMap<String, DCCAspectPanel> dccAspect = new HashMap<String, DCCAspectPanel>(10);

    void dccUnLitPanel() {
        dccUnLitPanel.setLayout(new BoxLayout(dccUnLitPanel, BoxLayout.Y_AXIS));
        JPanel dccDetails = new JPanel();
        dccDetails.add(new JLabel(Bundle.getMessage("DCCMastSetAspectId")));
        dccDetails.add(unLitAspectField);
        unLitAspectField.setText("31");
        dccUnLitPanel.add(dccDetails);
        TitledBorder border = BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.black));
        border.setTitle(Bundle.getMessage("DCCUnlitAspectNumber"));
        dccUnLitPanel.setBorder(border);
        unLitAspectField.addFocusListener(new FocusListener() {
            public void focusLost(FocusEvent e) {
                if (unLitAspectField.getText().equals("")) {
                    return;
                }
                if (!validateAspectId(unLitAspectField.getText())) {
                    unLitAspectField.requestFocusInWindow();
                }
            }

            public void focusGained(FocusEvent e) {
            }

        });
    }

    void updateDCCMastPanel() {
        if ((!Bundle.getMessage("DCCMast").equals(signalMastDriver.getSelectedItem())) && (!Bundle.getMessage("LNCPMast").equals(signalMastDriver.getSelectedItem()))) {
            return;
        }
        dccAspect = new HashMap<String, DCCAspectPanel>(10);
        java.util.List<jmri.CommandStation> connList = jmri.InstanceManager.getList(jmri.CommandStation.class);
        systemPrefixBox.removeAllItems();
        if (connList != null) {
            for (int x = 0; x < connList.size(); x++) {
                jmri.CommandStation station = connList.get(x);
                if (Bundle.getMessage("LNCPMast").equals(signalMastDriver.getSelectedItem())) {
                    if (station instanceof jmri.jmrix.loconet.SlotManager) {
                        systemPrefixBox.addItem(station.getUserName());
                    }
                } else {
                    systemPrefixBox.addItem(station.getUserName());
                }
            }
        } else {
            systemPrefixBox.addItem("None");
        }
        String mastType = mastNames.get(mastBox.getSelectedIndex()).getName();
        mastType = mastType.substring(11, mastType.indexOf(".xml"));
        jmri.implementation.DefaultSignalAppearanceMap sigMap = jmri.implementation.DefaultSignalAppearanceMap.getMap(sigsysname, mastType);
        java.util.Enumeration<String> aspects = sigMap.getAspects();
        SignalSystem sigsys = InstanceManager.signalSystemManagerInstance().getSystem(sigsysname);
        while (aspects.hasMoreElements()) {
            String aspect = aspects.nextElement();
            DCCAspectPanel aPanel = new DCCAspectPanel(aspect);
            dccAspect.put(aspect, aPanel);
            aPanel.setAspectId((String) sigsys.getProperty(aspect, "dccAspect"));
        }
        dccMastPanel.removeAll();
        dccMastPanel.setLayout(new jmri.util.javaworld.GridLayout2(dccAspect.size() + 3, 2));
        dccMastPanel.add(systemPrefixBoxLabel);
        dccMastPanel.add(systemPrefixBox);
        dccMastPanel.add(dccAspectAddressLabel);
        dccMastPanel.add(dccAspectAddressField);
        if (dccAddressListener == null) {
            dccAddressListener = new FocusListener() {
                public void focusLost(FocusEvent e) {
                    if (dccAspectAddressField.getText().equals("")) {
                        return;
                    }
                    validateDCCAddress();
                }

                public void focusGained(FocusEvent e) {
                }

            };

            dccAspectAddressField.addFocusListener(dccAddressListener);
        }

        if (mast == null) {
            systemPrefixBoxLabel.setEnabled(true);
            systemPrefixBox.setEnabled(true);
            dccAspectAddressLabel.setEnabled(true);
            dccAspectAddressField.setEnabled(true);
        }

        for (String aspect : dccAspect.keySet()) {
            dccMastPanel.add(dccAspect.get(aspect).getPanel());
        }
        if ((dccAspect.size() & 1) == 1) {
            dccMastPanel.add(new JLabel());
        }
        dccMastPanel.add(new JLabel(Bundle.getMessage("DCCMastCopyAspectId")));
        dccMastPanel.add(copyFromMastSelection());

    }

    FocusListener dccAddressListener = null;

    static boolean validateAspectId(String strAspect) {
        int aspect = -1;
        try {
            aspect = Integer.parseInt(strAspect.trim());
        } catch (java.lang.NumberFormatException e) {
            JOptionPane.showMessageDialog(null, Bundle.getMessage("DCCMastAspectNumber"));
            return false;
        }

        if (aspect < 0 || aspect > 31) {
            JOptionPane.showMessageDialog(null, Bundle.getMessage("DCCMastAspectOutOfRange"));
            log.error("invalid aspect " + aspect);
            return false;
        }
        return true;
    }

    boolean validateDCCAddress() {
        if (dccAspectAddressField.getText().equals("")) {
            JOptionPane.showMessageDialog(null, Bundle.getMessage("DCCMastAddressBlank"));
            return false;
        }
        int address = -1;
        try {
            address = Integer.parseInt(dccAspectAddressField.getText().trim());
        } catch (java.lang.NumberFormatException e) {
            JOptionPane.showMessageDialog(null, Bundle.getMessage("DCCMastAddressNumber"));
            return false;
        }

        if (address < NmraPacket.accIdLowLimit || address > NmraPacket.accIdAltHighLimit) {
            JOptionPane.showMessageDialog(null, Bundle.getMessage("DCCMastAddressOutOfRange"));
            log.error("invalid address " + address);
            return false;
        }
        if (DccSignalMast.isDCCAddressUsed(address) != null) {
            String msg = Bundle.getMessage("DCCMastAddressAssigned", new Object[]{dccAspectAddressField.getText(), DccSignalMast.isDCCAddressUsed(address)});
            JOptionPane.showMessageDialog(null, msg);
            return false;
        }
        return true;
    }

    JComboBox<String> copyFromMastSelection() {
        JComboBox<String> mastSelect = new JComboBox<String>();
        List<String> names = InstanceManager.signalMastManagerInstance().getSystemNameList();
        for (String name : names) {
            if ((InstanceManager.signalMastManagerInstance().getNamedBean(name) instanceof DccSignalMast)
                    && InstanceManager.signalMastManagerInstance().getSignalMast(name).getSignalSystem().getSystemName().equals(sigsysname)) {
                mastSelect.addItem(InstanceManager.signalMastManagerInstance().getNamedBean(name).getDisplayName());
            }
        }
        if (mastSelect.getItemCount() == 0) {
            mastSelect.setEnabled(false);
        } else {
            mastSelect.insertItemAt("", 0);
            mastSelect.setSelectedIndex(0);
            mastSelect.addActionListener(new ActionListener() {
                @SuppressWarnings("unchecked") // e.getSource() cast from mastSelect source
                public void actionPerformed(ActionEvent e) {
                    JComboBox<String> eb = (JComboBox<String>) e.getSource();
                    String sourceMast = (String) eb.getSelectedItem();
                    if (sourceMast != null && !sourceMast.equals("")) {
                        copyFromAnotherDCCMastAspect(sourceMast);
                    }
                }
            });
        }
        return mastSelect;
    }

    void copyFromAnotherDCCMastAspect(String strMast) {
        DccSignalMast mast = (DccSignalMast) InstanceManager.signalMastManagerInstance().getNamedBean(strMast);
        for (String aspect : dccAspect.keySet()) {
            if (mast.isAspectDisabled(aspect)) {
                dccAspect.get(aspect).setAspectDisabled(true);
            } else {
                dccAspect.get(aspect).setAspectId(mast.getOutputForAppearance(aspect));
            }
        }
    }

    static class DCCAspectPanel {

        String aspect = "";
        JCheckBox disabledCheck = new JCheckBox(Bundle.getMessage("DisableAspect"));
        JLabel aspectLabel = new JLabel(Bundle.getMessage("DCCMastSetAspectId"));
        JTextField aspectId = new JTextField(5);

        DCCAspectPanel(String aspect) {
            this.aspect = aspect;
        }

        void setAspectDisabled(boolean boo) {
            disabledCheck.setSelected(boo);
            if (boo) {
                aspectLabel.setEnabled(false);
                aspectId.setEnabled(false);
            } else {
                aspectLabel.setEnabled(true);
                aspectId.setEnabled(true);
            }
        }

        boolean isAspectDisabled() {
            return disabledCheck.isSelected();
        }

        int getAspectId() {
            try {
                String value = aspectId.getText();
                return Integer.parseInt(value);

            } catch (Exception ex) {
                log.error("failed to convert DCC number");
            }
            return -1;
        }

        void setAspectId(int i) {
            aspectId.setText("" + i);
        }

        void setAspectId(String s) {
            aspectId.setText(s);
        }

        JPanel panel;

        JPanel getPanel() {
            if (panel == null) {
                panel = new JPanel();
                panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
                JPanel dccDetails = new JPanel();
                dccDetails.add(aspectLabel);
                dccDetails.add(aspectId);
                panel.add(dccDetails);
                panel.add(disabledCheck);
                TitledBorder border = BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.black));
                border.setTitle(aspect);
                panel.setBorder(border);
                aspectId.addFocusListener(new FocusListener() {
                    public void focusLost(FocusEvent e) {
                        if (aspectId.getText().equals("")) {
                            return;
                        }
                        if (!validateAspectId(aspectId.getText())) {
                            aspectId.requestFocusInWindow();
                        }
                    }

                    public void focusGained(FocusEvent e) {
                    }

                });
                disabledCheck.addActionListener(new ActionListener() {
                    public void actionPerformed(ActionEvent e) {
                        setAspectDisabled(disabledCheck.isSelected());
                    }
                });

            }
            return panel;
        }

    }

    void updateMatrixAspectPanel() { // EBR
        if (!Bundle.getMessage("MatrixCtlMast").equals(signalMastDriver.getSelectedItem())) {
            return;
        }
        String bitString = "00000"; // make from mast(aspect) EBR
        matrixAspect = new HashMap<String, MatrixAspectPanel>(10);
        String mastType = mastNames.get(mastBox.getSelectedIndex()).getName();
        mastType = mastType.substring(11, mastType.indexOf(".xml"));
        jmri.implementation.DefaultSignalAppearanceMap sigMap = jmri.implementation.DefaultSignalAppearanceMap.getMap(sigsysname, mastType);
        java.util.Enumeration<String> aspects = sigMap.getAspects();
        while (aspects.hasMoreElements()) {
            String aspect = aspects.nextElement();
            MatrixAspectPanel aPanel = new MatrixAspectPanel(aspect, bitString); // build 1 line, include bitString?
            matrixAspect.put(aspect, aPanel);
        }

        matrixMastPanel.removeAll();
        matrixMastPanel.setLayout(new jmri.util.javaworld.GridLayout2(matrixAspect.size() + 1, 2));
        for (String aspect : matrixAspect.keySet()) {
            matrixMastPanel.add(matrixAspect.get(aspect).getPanel());
            // repeat Matrix checkboxes in getPanel
        }

        matrixMastPanel.add(resetPreviousState); //
        resetPreviousState.setToolTipText(Bundle.getMessage("ResetPreviousToolTip"));
    }

    //ArrayList<JmriBeanComboBox> headList = ArrayList<JmriBeanComboBox>(5); // allready defined heads? EBR

    JPanel matrixUnLitPanel = new JPanel();

    //String stateThrown = InstanceManager.turnoutManagerInstance().getThrownText();
    //String stateClosed = InstanceManager.turnoutManagerInstance().getClosedText();
    //String[] turnoutStates = new String[]{stateClosed, stateThrown};
    //int[] turnoutStateValues = new int[]{Turnout.CLOSED, Turnout.THROWN};
    // already defined

    BeanSelectCreatePanel matrixUnLitBox = new BeanSelectCreatePanel(InstanceManager.turnoutManagerInstance(), null);
    JComboBox<String> matrixUnLitState = new JComboBox<String>(turnoutStates);
    BeanSelectCreatePanel turnout1Box = new BeanSelectCreatePanel(InstanceManager.turnoutManagerInstance(), null);
    BeanSelectCreatePanel turnout2Box = new BeanSelectCreatePanel(InstanceManager.turnoutManagerInstance(), null);
    BeanSelectCreatePanel turnout3Box = new BeanSelectCreatePanel(InstanceManager.turnoutManagerInstance(), null);
    BeanSelectCreatePanel turnout4Box = new BeanSelectCreatePanel(InstanceManager.turnoutManagerInstance(), null);
    BeanSelectCreatePanel turnout5Box = new BeanSelectCreatePanel(InstanceManager.turnoutManagerInstance(), null);
    // no states, on = thrown, off = closed

    void matrixUnLitPanel() {
        matrixUnLitPanel.setLayout(new BoxLayout(matrixUnLitPanel, BoxLayout.Y_AXIS));
        JPanel matrixDetails = new JPanel();
        // number of columns
        int bitNum = 5; // default to 5 col
        bitNumSpinner = new JSpinner(new SpinnerNumberModel(bitNum, 1, 5, 1));
//        bitNumSpinner.addChangeListener((ItemEvent e) -> {
//            bitNum = bitNumSpinner.getValue();
//            updateMatrixAspectPanel(); // hide/show last cols in matrix
//        });
        matrixDetails.add(bitNumSpinner);
        // repeat next line 5 x for output turnouts
        // binary matrix outputs go here
        // ToDo: for bitNum loop
        matrixDetails.add(turnout1Box);
        if (bitNum > 1) {
            matrixDetails.add(turnout2Box);
        }
        if (bitNum > 2) {
            matrixDetails.add(turnout3Box);
        }
        if (bitNum > 3) {
            matrixDetails.add(turnout4Box);
        }
        if (bitNum > 4) {
            matrixDetails.add(turnout5Box);
        }
        // ToDo: add boxes for DCC Packets
        matrixDetails.add(turnoutUnLitBox);
        matrixDetails.add(new JLabel(Bundle.getMessage("SetState")));
        matrixDetails.add(turnoutUnLitState);
        matrixUnLitPanel.add(matrixDetails);
        TitledBorder border = BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.black));
        border.setTitle(Bundle.getMessage("TurnUnLitDetails"));
        matrixUnLitPanel.setBorder(border);
    }

    HashMap<String, MatrixAspectPanel> matrixAspect = new HashMap<String, MatrixAspectPanel>(10);

    class MatrixAspectPanel {

        JCheckBox disabledCheck = new JCheckBox(Bundle.getMessage("DisableAspect"));
        JCheckBox bitCheck1 = new JCheckBox();
        JCheckBox bitCheck2 = new JCheckBox();
        JCheckBox bitCheck3 = new JCheckBox();
        JCheckBox bitCheck4 = new JCheckBox();
        JCheckBox bitCheck5 = new JCheckBox();

        String aspect = "";

        MatrixAspectPanel(String aspect) {
            this.aspect = aspect;
        }

        MatrixAspectPanel(String aspect, String bitString) {
            if (bitString == null || bitString.equals("")) {
                return;
            }
            this.aspect = aspect;
            // bitString is string of length (bitNum) describing state of on/off checkboxes
            // convert to states?
            int bitnum = bitString.length();
                bitCheck1.setSelected(bitString.substring(0, 1) == "1");
            if (bitNum > 1) {
                bitCheck2.setSelected(bitString.substring(1, 2) == "1");
            }
            // repeat for each char in bitString // todo
        }

        void setReference(String reference) {
            bitCheck1.setReference(reference); // EBR was turnout, should be/
        }

        void setAspectDisabled(boolean boo) {
            disabledCheck.setSelected(boo);
            if (boo) {
                bitCheck1.setEnabled(false);
                if (bitCheck2.isVisible()) {
                    bitCheck2.setEnabled(false);
                }
                if (bitCheck3.isVisible()) {
                    bitCheck3.setEnabled(false);
                }
                if (bitCheck4.isVisible()) {
                    bitCheck4.setEnabled(false);
                }
                if (bitCheck5.isVisible()) {
                    bitCheck5.setEnabled(false);
                }
            } else {
                bitCheck1.setEnabled(true);
                if (bitCheck2.isVisible()) {
                    bitCheck2.setEnabled(true);
                }
                if (bitCheck3.isVisible()) {
                    bitCheck3.setEnabled(true);
                }
                if (bitCheck4.isVisible()) {
                    bitCheck4.setEnabled(true);
                }
                if (bitCheck5.isVisible()) {
                    bitCheck5.setEnabled(true);
                }
            }
        }

        boolean isAspectDisabled() {
            return disabledCheck.isSelected();
        }

        JPanel panel;

        JPanel getPanel() {
            // build Aspect Matrix row
            if (panel == null) {
                panel = new JPanel();
                panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
                panel.add(disabledCheck); // before checkboxes, not below
                JPanel matrixDetails = new JPanel();
                matrixDetails.add(bitCheck1);
//                bitCheck1.addItemListener(new ItemListener()) {
//                    @Override
//                    public void itemStateChanged(ItemEvent e) {
//                        // ToDo refresh aspectSetting EBR, can be in OK to store/warn for duplicates
//                    }
//                }
                matrixDetails.add(bitCheck2);
                matrixDetails.add(bitCheck3);
                matrixDetails.add(bitCheck4);
                matrixDetails.add(bitCheck5);
                panel.add(matrixDetails);
                // panel.add(disabledCheck); // here in TurnoutSignalMast
                TitledBorder border = BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.black));
                border.setTitle(aspect);
                panel.setBorder(border);

                disabledCheck.addActionListener(new ActionListener() {
                    public void actionPerformed(ActionEvent e) {
                        setAspectDisabled(disabledCheck.isSelected());
                    }
                });

            }
            return panel;
        }

    }

    private final static Logger log = LoggerFactory.getLogger(AddSignalMastPanel.class.getName());
}


/* @(#)SensorTableAction.java */
