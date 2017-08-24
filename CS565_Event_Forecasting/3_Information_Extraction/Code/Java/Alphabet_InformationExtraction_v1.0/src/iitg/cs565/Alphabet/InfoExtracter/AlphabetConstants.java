/*
 * Configuration parameters use in program.
 */
package iitg.cs565.Alphabet.InfoExtracter;

/**
 *
 * @author Neelesh
 */
public class AlphabetConstants {
    
    // Path of the protest articles filtered from LDA
    public static String PROTEST_ARTICLES_PATH = "D:\\IITG\\Sem2\\CS565\\Project\\Final_Project\\2_Event_Filtering\\Data\\LDA_Filtered_Articles\\";
    
    // Output Directory location for Tagged Protest Articles
    public static String TAGGED_PROTEST_ARTICLES_PATH = "D:\\IITG\\Sem2\\CS565\\Project\\Final_Project\\3_Information_Extraction\\Data\\Tagged_Protest_Articles\\";
    
    // Output directory loction for Relations
    public static String RELATION_PATH = "D:\\IITG\\Sem2\\CS565\\Project\\Final_Project\\3_Information_Extraction\\Data\\Relations\\";
    
    public static int LARGEST_FILE_INDEX = 73000;
    
    // Flag controls execution of NER Tagger
    public static int RUN_NER_TAGGER = 1;
    
    // Flag controls execution of Relation Builder
    public static int RUN_RELATION_BUILDER = 1;
    
  
}
