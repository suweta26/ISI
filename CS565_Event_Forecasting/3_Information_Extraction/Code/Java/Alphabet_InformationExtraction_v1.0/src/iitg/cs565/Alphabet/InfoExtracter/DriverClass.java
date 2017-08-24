/**
 * Driver program to run NER tagger and Relation extractor.
 * 
 */

package iitg.cs565.Alphabet.InfoExtracter;

/**
 *
 * @author Neelesh
 */
public class DriverClass {
    
    
    public static void main(String...args) throws Exception
    {
        // Run NER Tagger
        if(AlphabetConstants.RUN_NER_TAGGER == 1)
        {
            NERTagger ner = new NERTagger();
            ner.tagEntity();
        }
        
         // Run Relation Builder
        if(AlphabetConstants.RUN_RELATION_BUILDER == 1)
        {
            RealationBuilder rex = new RealationBuilder();
            rex.buildAllRelations();
        }
    }
    
}
