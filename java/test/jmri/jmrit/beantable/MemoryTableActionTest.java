package jmri.jmrit.beantable;

import java.awt.GraphicsEnvironment;
import javax.swing.JFrame;
import javax.swing.JTextField;
import jmri.util.JUnitUtil;
import org.junit.*;
import org.netbeans.jemmy.operators.*;

/**
 * Tests for classes in the jmri.jmrit.beantable package
 *
 * @author	Bob Jacobsen Copyright 2004
 */
public class MemoryTableActionTest extends AbstractTableActionBase {

    @Test
    public void testCreate() {
        Assert.assertNotNull(a);
    }

    @Override
    public String getTableFrameName(){
       return Bundle.getMessage("TitleMemoryTable");
    }

    @Override
    @Test
    public void testGetClassDescription(){
         Assert.assertEquals("Memory Table Action class description","Memory Table",a.getClassDescription());
    }

    /**
     * Check the return value of includeAddButton.  The table generated by 
     * this action includes an Add Button.
     */
    @Override
    @Test
    public void testIncludeAddButton(){
         Assert.assertTrue("Default include add button",a.includeAddButton());
    }

    @Override
    public String getAddFrameName(){
        return Bundle.getMessage("TitleAddMemory");
    }

    @Test
    @Override
    public void testAddThroughDialog() {
        Assume.assumeFalse(GraphicsEnvironment.isHeadless());
        Assume.assumeTrue(a.includeAddButton());
        a.actionPerformed(null);
        JFrame f = JFrameOperator.waitJFrame(getTableFrameName(), true, true);

        // find the "Add... " button and press it.
	jmri.util.swing.JemmyUtil.pressButton(new JFrameOperator(f),Bundle.getMessage("ButtonAdd"));
        new org.netbeans.jemmy.QueueTool().waitEmpty();
        JFrame f1 = JFrameOperator.waitJFrame(getAddFrameName(), true, true);
        JFrameOperator jf = new JFrameOperator(f1);
	    //Enter 1 in the text field labeled "System Name:"
        JLabelOperator jlo = new JLabelOperator(jf,Bundle.getMessage("LabelSystemName"));
        ((JTextField)jlo.getLabelFor()).setText("1");
	    //and press create
	    jmri.util.swing.JemmyUtil.pressButton(jf,Bundle.getMessage("ButtonCreate"));
        JUnitUtil.dispose(f1);
        JUnitUtil.dispose(f);
    }

    @Test
    @Ignore("no Edit button in memory Table")
    @Override
    public void testEditButton() {
    }


    @Before
    @Override
    public void setUp() {
        JUnitUtil.setUp();
        jmri.util.JUnitUtil.resetProfileManager();
        jmri.util.JUnitUtil.initDefaultUserMessagePreferences();
        helpTarget = "package.jmri.jmrit.beantable.MemoryTable"; 
        a = new MemoryTableAction();
    }

    @After
    @Override
    public void tearDown() {
        JUnitUtil.tearDown();
        a = null;
    }

}
