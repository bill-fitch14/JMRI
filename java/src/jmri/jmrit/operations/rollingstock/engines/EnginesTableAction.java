// EnginesTableAction.java
package jmri.jmrit.operations.rollingstock.engines;

import java.awt.event.ActionEvent;
import javax.swing.AbstractAction;

/**
 * Swing action to create and register a EnginesTableFrame object.
 *
 * @author Bob Jacobsen Copyright (C) 2001
 * @author Daniel Boudreau Copyright (C) 2008
 * @version $Revision$
 */
public class EnginesTableAction extends AbstractAction {

    /**
     *
     */
    private static final long serialVersionUID = 755025320493011103L;

    public EnginesTableAction(String s) {
        super(s);
    }

    public EnginesTableAction() {
        this(Bundle.getMessage("MenuEngines")); // NOI18N
    }

    public void actionPerformed(ActionEvent e) {
        // create a engine table frame
        new EnginesTableFrame();
    }
}

/* @(#)EnginesTableAction.java */
