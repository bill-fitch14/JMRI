package jmri.jmrit.z21server;

import jmri.InstanceManager;
import jmri.ThrottleManager;
import jmri.jmrit.z21server.UserInterface;
import jmri.util.swing.JmriAbstractAction;
import jmri.util.swing.WindowInterface;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;

/**
 * Start, and create if needed, the WiThrottle server.
 *
 * @author Brett Hoffman Copyright (C) 2009
 *
 */
public class z21serverCreationAction extends JmriAbstractAction {

    public z21serverCreationAction(String s, WindowInterface wi) {
        super(s, wi);
    }

    public z21serverCreationAction(String s, Icon i, WindowInterface wi) {
        super(s, i, wi);
    }

    /**
     * Create a new network server.
     *
     * @param name Labels frame in GUI
     */
    public z21serverCreationAction(String name) {
        super(name);
        if (InstanceManager.getNullableDefault(ThrottleManager.class) == null) {
            super.setEnabled(false);
        }
    }

    /**
     * Create a new network server.
     */
    public z21serverCreationAction() {
        this(Bundle.getMessage("MenuStartz21serverServer"));
    }

    /**
     * Start the server end.
     *
     * @param e The event causing the action.
     */
    @Override
    public void actionPerformed(ActionEvent e) {

        FacelessServer server = FacelessServer.getInstance();
        server.start();

        // ensure the GUI is visible if we are not in headless mode.
        if (!GraphicsEnvironment.isHeadless()) {
            UserInterface ui = InstanceManager.getOptionalDefault(UserInterface.class).orElseGet(() -> {
                return InstanceManager.setDefault(UserInterface.class, new UserInterface());
            });
            ui.setVisible(true);
        }
    }

    // never invoked, because we overrode actionPerformed above
    @Override
    public jmri.util.swing.JmriPanel makePanel() {
        throw new IllegalArgumentException("Should not be invoked");
    }

}
