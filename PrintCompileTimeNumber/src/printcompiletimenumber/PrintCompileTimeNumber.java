/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package printcompiletimenumber;

import java.io.File;
import java.util.Map;
import java.util.jar.Attributes;
import java.util.jar.JarFile;
import java.util.jar.Manifest;

/**
 * This program is designed to display a number when run after being
 * compiled with ant.  To set this number:
 * 
 * ant -Dbuildnum="21"
 * 
 * If the value is -1,  it was probably built without setting that value.
 * This is used in the testing of Jenkins so that the test can verify the
 * artifact (jar file) is produced from the latest build and isn't an old 
 * version.
 * 
 * @author keithstegbauer
 */
public class PrintCompileTimeNumber {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        try {
            File currentFile = new File(PrintCompileTimeNumber.class.getProtectionDomain().getCodeSource().getLocation().toURI().getPath());
            JarFile myJar = new JarFile(currentFile);
            Manifest manifest = myJar.getManifest();            
            Map<String,Attributes> manifestContents = manifest.getEntries();
            Attributes bldnum;
            bldnum = manifest.getMainAttributes();            
            System.out.println(bldnum.getValue("Build-Number"));
        } catch (Exception e) {
            e.printStackTrace();            
        }
    }
    
}
