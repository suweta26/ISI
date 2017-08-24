/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package iitg.cs565.Alphabet.InfoExtracter;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.ie.util.RelationTriple;
import edu.stanford.nlp.naturalli.NaturalLogicAnnotations;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Collection;
import java.util.Properties;

/**
 *
 * @author Neelesh
 */
public class RealationBuilder {

    public void buildAllRelations() {
        try {
            Properties props = new Properties();
            props.setProperty("annotators", "tokenize,ssplit,pos,lemma,depparse,natlog,openie");
            StanfordCoreNLP core = new StanfordCoreNLP(props);

            System.out.println("Stanford Core NLP Initialized");

            BufferedReader br = null;
            PrintWriter pw = null;
            String line;
            int fileIndex = 1;

            for (; fileIndex < AlphabetConstants.LARGEST_FILE_INDEX; fileIndex++) {
                StringBuffer inFilePath = new StringBuffer();
                StringBuffer outFilePath = new StringBuffer();
                inFilePath.append(AlphabetConstants.TAGGED_PROTEST_ARTICLES_PATH).append(fileIndex);
                outFilePath.append(AlphabetConstants.RELATION_PATH).append(fileIndex);

                File file = new File(inFilePath.toString());

                if (file.exists()) {
                    System.out.println("File exists: " + fileIndex);

                    // Read file                   
                    br = new BufferedReader(new FileReader(inFilePath.toString()));
                    pw = new PrintWriter(new FileWriter(outFilePath.toString()));

                    // Read all lines
                    while ((line = br.readLine()) != null) {

                        Annotation doc = new Annotation(line);
                        core.annotate(doc);

                        for (CoreMap sentence : doc.get(CoreAnnotations.SentencesAnnotation.class)) {
                            Collection<RelationTriple> triples = sentence.get(NaturalLogicAnnotations.RelationTriplesAnnotation.class);
                            for (RelationTriple triple : triples) {

                                pw.write("("
                                        + triple.subjectLemmaGloss() + "#"
                                        + triple.relationLemmaGloss() + "#"
                                        + triple.objectLemmaGloss() + ")\n");

                            }
                        }
                    }
                    br.close();;
                    pw.close();

                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
