// CreateRosterGroupAction.java
package jmri.jmrit.roster.swing;

import java.awt.Component;
import java.awt.event.ActionEvent;
import java.util.ArrayList;
import java.util.ResourceBundle;
import javax.swing.Icon;
import javax.swing.JOptionPane;
import jmri.jmrit.roster.Roster;
import jmri.jmrit.roster.RosterEntry;
import jmri.util.swing.JmriAbstractAction;
import jmri.util.swing.WindowInterface;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Create a roster group.
 *
 *
 * <hr>
 * This file is part of JMRI.
 * <P>
 * JMRI is free software; you can redistribute it and/or modify it under the
 * terms of version 2 of the GNU General Public License as published by the Free
 * Software Foundation. See the "COPYING" file for a copy of this license.
 * <P>
 * JMRI is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 * A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * <P>
 * @author	Kevin Dickerson Copyright (C) 2009
 * @version	$Revision$
 */
public class CreateRosterGroupAction extends JmriAbstractAction {

    /**
     *
     */
    private static final long serialVersionUID = -8222098783980850363L;

    public CreateRosterGroupAction(String s, WindowInterface wi) {
        super(s, wi);
    }

    public CreateRosterGroupAction(String s, Icon i, WindowInterface wi) {
        super(s, i, wi);
    }

    /**
     * @param s   Name of this action, e.g. in menus
     * @param who Component that action is associated with, used to ensure
     *            proper position in of dialog boxes
     */
    public CreateRosterGroupAction(String s, Component who) {
        super(s);
        _who = who;
    }

    Component _who;
    ArrayList<RosterEntry> rosterEntries;

    @Override
    public void actionPerformed(ActionEvent event) {

        String entry = (String) JOptionPane.showInputDialog(_who,
                "<html><b>" + ResourceBundle.getBundle("jmri.jmrit.roster.JmritRosterBundle").getString("MenuGroupCreate") + "</b></html>",
                ResourceBundle.getBundle("jmri.jmrit.roster.JmritRosterBundle").getString("MenuGroupCreate"),
                JOptionPane.INFORMATION_MESSAGE,
                null, // icon
                null, // initial values
                null);// preselected initial value
        if (entry == null || entry.equals(Roster.ALLENTRIES)) {
            return;
        }
        if (rosterEntries != null) {
            for (RosterEntry re : rosterEntries) {
                log.debug("Adding RosterEntry " + re.getId() + " to new group " + entry);
                re.putAttribute(Roster.instance().getRosterGroupPrefix() + entry, "yes");
                re.updateFile();
            }
        }
        Roster.instance().addRosterGroup(entry);
        Roster.writeRosterFile();
    }

    // never invoked, because we overrode actionPerformed above
    public jmri.util.swing.JmriPanel makePanel() {
        throw new IllegalArgumentException("Should not be invoked");
    }

    /**
     * Set a parameter
     * <p>
     * This method accepts the following key, with the following value:
     * <dl>
     * <dt>RosterEntries</dt>
     * <dd>An ArrayList&lt;RosterEntry&gt; of roster entries.
     * </dl>
     *
     * @param key
     * @param value
     */
    @Override
    @SuppressWarnings("unchecked")
    public void setParameter(String key, Object value) {
        if (key.equals("RosterEntries") && value.getClass().equals(ArrayList.class)) {
            rosterEntries = (ArrayList<RosterEntry>) value;
        }
    }

    // initialize logging
    private final static Logger log = LoggerFactory.getLogger(CreateRosterGroupAction.class.getName());
}
