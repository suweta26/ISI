/**
 * Read the result from relation extraction, normalize time and store into db.
 */


package iitg.cs565.Alphabet.TimeExpNormalizer;

import java.util.List;
import java.util.Properties;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.time.*;
import edu.stanford.nlp.util.CoreMap;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.text.SimpleDateFormat;

/**
 *
 * @author Neelesh
 */
public class AlphabetTimeExpression {

    
    public static void main(String[] args)
    {

        try 
        {
            // Load mysql driver
            Class.forName("com.mysql.jdbc.Driver");  
            // Create connection
            Connection con=DriverManager.getConnection("jdbc:mysql://"+AlphabetConstants.DB_SERVER+":"+AlphabetConstants.DB_PORT+"/"+AlphabetConstants.DB_NAME,AlphabetConstants.DB_USER_NAME,AlphabetConstants.DB_PASSWORD);  
            
            // Insert query to store data
            String insetSQL ="INSERT INTO `Events`(id,publish_date,title,persons,dates,organizations,locations) VALUE (?, ?, ?, ?, ?, ?, ?)";
            
                
                Properties props = new Properties();
                AnnotationPipeline pipeline = new AnnotationPipeline();
                pipeline.addAnnotator(new TokenizerAnnotator(false));
                pipeline.addAnnotator(new WordsToSentencesAnnotator(false));
                pipeline.addAnnotator(new POSTaggerAnnotator(false));
                pipeline.addAnnotator(new TimeAnnotator("sutime", props));
                
                SimpleDateFormat fromCoreNLP = new SimpleDateFormat("yyyy-MM-dd");
                SimpleDateFormat myFormat = new SimpleDateFormat("dd-MM-yyyy");

                File folder = new File(AlphabetConstants.RESULT_PATH);
                File[] listOfFiles = folder.listFiles();
                for (File file : listOfFiles)
                {
                if (file.isFile()) 
                {
                System.out.println(file.getName());
                FileReader fileReader = new FileReader(file);
                BufferedReader bufferedReader = new BufferedReader(fileReader);
                String pub_date=bufferedReader.readLine();
                String Title=bufferedReader.readLine();
                String persons=bufferedReader.readLine();
                String dateArr[]=bufferedReader.readLine().split(",\\s");
                String organisations=bufferedReader.readLine();
                String locations=bufferedReader.readLine();
                StringBuilder dates=new StringBuilder();
                int flag = 0; 
                for (String date : dateArr)
                {
                    String temp;
                    if(flag == 1)
                    {
                    dates.append(", ");
                    }
                try
                {
                Annotation annotation = new Annotation(date);
                annotation.set(CoreAnnotations.DocDateAnnotation.class, pub_date);
                pipeline.annotate(annotation);
                temp = annotation.get(CoreAnnotations.TextAnnotation.class);
                List<CoreMap> timexAnnsAll = annotation.get(TimeAnnotations.TimexAnnotations.class);
                for (CoreMap cm : timexAnnsAll) {
                    temp = cm.get(TimeExpression.Annotation.class).getTemporal().getTimexValue();
                    //temp = myFormat.format(fromCoreNLP.parse(temp));
                    
                }
                dates.append(temp);
                flag=1;
                 
                }
                catch(Exception e)
                {
                temp = "none";
                }
                }
                
                PreparedStatement pstmt = con.prepareStatement(insetSQL);
                pstmt.setInt(1, Integer.parseInt(file.getName()));
                pstmt.setString(2, pub_date);
                pstmt.setString(3, Title);
                pstmt.setString(4, persons);
                System.out.println(dates.toString());
                pstmt.setString(5, dates.toString());
                pstmt.setString(6, organisations);
                pstmt.setString(7, locations);
                pstmt.executeUpdate();
               
            }
        }
        
                
         con.close();
        } catch (Exception ex) {
            ex.printStackTrace();;
        }
    }

}
