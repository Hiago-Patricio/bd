package jasperreport.to.pdf;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;

import net.sf.jasperreports.engine.JRException;
import net.sf.jasperreports.engine.JRExporter;
import net.sf.jasperreports.engine.JRExporterParameter;
import net.sf.jasperreports.engine.JasperCompileManager;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.export.JRPdfExporter;

import jasperreport.to.pdf.ConnectionFactory;

/**
 * This article in 'pt_BR' teaches how to generate PDF reports on the Web with JasperReports
 * http://blog.triadworks.com.br/jasperreports-gerando-relatorios-pdf-na-web
 *
 * You'll need these jar's below:
 *	
 * jasperreports-5.0.1.jar
 * iText-2.1.7.jar (needed to generate PDF)
 * jfreechart-1.0.12.jar (needed to graphics and charts)
 * jcommon-1.0.15.jar (needed to graphics and charts)
 * commons-beanutils-1.8.2.jar
 * commons-collections-3.2.1.jar
 * commons-digester-2.1.jar
 * commons-logging-1.1.jar
 */
public class NewMain {

	public static void main(String[] args) {
		
		Connection connection = null;
		try {
		
			String reportName = "relatorio";
			Map<String, Object> parameters = new HashMap<String, Object>();
			connection = new ConnectionFactory().getConnection(); // opens a jdbc connection
			// fills compiled report with parameters and a connection
			JasperPrint print = JasperFillManager.fillReport(reportName + ".jasper", parameters, connection);
			// exports report to pdf
			JRExporter exporter = new JRPdfExporter();
			exporter.setParameter(JRExporterParameter.JASPER_PRINT, print);
			exporter.setParameter(JRExporterParameter.OUTPUT_STREAM, new FileOutputStream(reportName + ".pdf")); // your output goes here
			
			exporter.exportReport();

		} catch (Exception e) {
			throw new RuntimeException("It's not possible to generate the pdf report.", e);
		} finally {
			// it's your responsibility to close the connection, don't forget it!
			if (connection != null) {
				try { connection.close(); } catch (Exception e) {}
			}
		}
		
	}
	
}