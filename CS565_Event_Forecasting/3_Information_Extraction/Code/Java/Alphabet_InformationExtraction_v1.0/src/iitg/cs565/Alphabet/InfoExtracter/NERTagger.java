/*
 * This is which reads a text from file and tags entities.
 * We are using Stanford NER Tagger with 7 class tagger
 * 7 Classes are: PERSON LOCATION DATE TIME ORGANIZATION MISC NUMBER
 */
package iitg.cs565.Alphabet.InfoExtracter;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import java.util.Properties;

import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.util.CoreMap;

import java.io.File;
import java.io.FileInputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Neelesh
 */
public class NERTagger {

    // Method to tag PERSON, LOCATION, DATE
    public void tagEntity() throws Exception {

        try {
            Properties props = new Properties();
            
            boolean useRegexner = true;
            
            // Put all the models that needs to be used
            if (useRegexner) {
                props.put("annotators", "tokenize, ssplit, pos, lemma, ner");
                props.put("regexner.mapping", "locations.txt");
            } else {
                props.put("annotators", "tokenize, ssplit, pos, lemma, ner");
            }
            
            StanfordCoreNLP core = new StanfordCoreNLP(props);
            
            System.out.println("Stanford Core NLP Initialized");
           
            int fileIndex = 1;
            
            // Iterate over all the files
            while (fileIndex <= AlphabetConstants.LARGEST_FILE_INDEX) {
                System.out.println("Inside file number " + fileIndex);
                StringBuilder inpuFilePath = new StringBuilder();
                inpuFilePath.append(AlphabetConstants.PROTEST_ARTICLES_PATH).append(fileIndex);
                String path_to_write = AlphabetConstants.TAGGED_PROTEST_ARTICLES_PATH + fileIndex;
                //System.out.println(inpuFilePath);
                File file = new File(inpuFilePath.toString());
                if (file.exists()) {
                    System.out.println("FileExist " + fileIndex);
                    FileInputStream fis = new FileInputStream(file);
                    byte[] fileContent = new byte[(int) file.length()];
                    fis.read(fileContent);
                    fis.close();
                    System.out.println(fileIndex);

                    // Get the file content
                    String fileContentUTF8 = new String(fileContent, "UTF-8");

                    String[] sentenceArray = {""};
                    String taggedText = "";
                    int i = 0;
                    
                    // Stanford tagger runs for only sentences so splitting the file content
                    String splitFileContent[] = fileContentUTF8.split("\n");
                    
                    while (i < splitFileContent.length) {
                        sentenceArray[0] = splitFileContent[i];
                        i++;

                        List tokens = new ArrayList<>();
                        
                        // For each sentence in the sentence list 
                        for (String s : sentenceArray) {
                            // Annotate the sentence
                            Annotation document = new Annotation(s);
                            core.annotate(document);
                            List<CoreMap> sentences = document.get(CoreAnnotations.SentencesAnnotation.class);
                            StringBuilder sb = new StringBuilder();
                            for (CoreMap sentence : sentences) {
                                taggedText = taggedText + "\n";

                                String prevNeToken = "O";
                                String currNeToken;
                                boolean newToken = true;
                                int flag = 0;
                                
                                for (CoreLabel token : sentence.get(CoreAnnotations.TokensAnnotation.class)) {
                                    currNeToken = token.get(CoreAnnotations.NamedEntityTagAnnotation.class);
                                    String currWord = token.get(CoreAnnotations.TextAnnotation.class);

                                    // Skip O tags
                                    if ((currNeToken.equals("O"))) {
                                        if (!((flag == 0 && currWord.equals(".")))) {
                                            taggedText = taggedText + " " + currWord;
                                        }
                                        flag = 1;
                                    } else {
                                        currWord = currWord + "/" + currNeToken;
                                        taggedText = taggedText + " " + currWord;
                                        flag = 1;
                                    }
                                    if (currNeToken.equals("O")) {
                                        if (!prevNeToken.equals("O") && (sb.length() > 0)) {
                                            handleEntity(prevNeToken, sb, tokens);
                                            newToken = true;
                                        }
                                        continue;
                                    }

                                    if (newToken) {
                                        prevNeToken = currNeToken;
                                        newToken = false;
                                        sb.append(currWord);
                                        continue;
                                    }

                                    if (currNeToken.equals(prevNeToken)) {
                                        sb.append(" ").append(currWord);
                                    } else {
                                        handleEntity(prevNeToken, sb, tokens);
                                        newToken = true;
                                    }
                                    prevNeToken = currNeToken;

                                }
                            }
                        }

                    }

                    PrintWriter out1 = new PrintWriter(path_to_write);
                    out1.println(taggedText);
                    out1.close();

                } 
                fileIndex++;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private void handleEntity(String inKey, StringBuilder inSb, List inTokens) {

        inTokens.add(new EmbeddedToken(inKey, inSb.toString()));
        inSb.setLength(0);
    }

}

class EmbeddedToken {

    private String name;
    private String value;

    public String getName() {
        return name;
    }

    public String getValue() {
        return value;
    }

    public EmbeddedToken(String name, String value) {
        super();
        this.name = name;
        this.value = value;
    }
}
