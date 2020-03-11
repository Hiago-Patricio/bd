/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package jasperreport.to.pdf;

import java.sql.Connection;
import java.sql.DriverManager;

/**
 *
 * @author gustavo
 */
public class ConnectionFactory {

    Connection getConnection() {
                Connection connection = null;
        try{
            Class.forName("org.postgresql.Driver");
            connection = DriverManager.getConnection("jdbc:postgresql://postgres.czuc1renrprc.sa-east-1.rds.amazonaws.com/postgres", "postgres", "12345678");
        }catch(Exception erro){
            erro.printStackTrace(); 
        }
        
        return connection;
    }
}
