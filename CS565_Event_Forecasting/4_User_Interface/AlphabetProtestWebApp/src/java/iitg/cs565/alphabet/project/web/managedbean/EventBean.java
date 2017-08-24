/*
 * Web application to select events
 */
package iitg.cs565.alphabet.project.web.managedbean;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;

/**
 *
 * @author Neelesh
 */

@ManagedBean(name = "eventBean")
@RequestScoped
public class EventBean {
    
    private List<EventResult> results;
    private int eventCount=0;
    private String error;
    
    private Date date;
    
    public String getEvents()
    {
     System.out.println("DEBUGGING::::::::Inside Get events");
     System.out.println("DEBUGGING:::::::: Input Date is : "+date);
     results = new ArrayList<>();
    try
    {
     Class.forName("com.mysql.jdbc.Driver");  
            // Create connection
    Connection con=DriverManager.getConnection("jdbc:mysql://"+AlphabetConstants.DB_SERVER+":"+AlphabetConstants.DB_PORT+"/"+AlphabetConstants.DB_NAME,AlphabetConstants.DB_USER_NAME,AlphabetConstants.DB_PASSWORD);  
        Statement statement = con.createStatement();
    ResultSet result = statement.executeQuery(AlphabetConstants.SELECT_SQL);
    
    // Get all the events 
    while(result.next()) {
        
        // Process each event
        int eventId = result.getInt(AlphabetConstants.COL_ID);
        String eventTitle = result.getString(AlphabetConstants.COL_TITLE);
        String persons = result.getString(AlphabetConstants.COL_PERSONS);
        String organizations = result.getString(AlphabetConstants.COL_ORGANIZATIONS);
        String locations = result.getString(AlphabetConstants.COL_LOCATIONS);
        String dates = result.getString(AlphabetConstants.COL_DATES);
        
        dates = processDates(dates);
        if(!dates.equalsIgnoreCase(""))
        {
        EventResult res = new EventResult(eventId, eventTitle, persons, organizations, locations, dates);
        results.add(res);
        }

}
    }
    catch(Exception e)
    {
        e.printStackTrace();
    }
    return "success";
    }
    
    // Get the dates of event and filter those dates which are greater than input date
    private String processDates(String dates) throws ParseException
    {
        String dateArr[]=dates.split(",\\s");
        String returnDates="";
        int flag =0;
        
        SimpleDateFormat myFormat = new SimpleDateFormat("dd-MM-yyyy");
        
        if(date==null)
            date = new Date(1483209000000L);
       Date input_date = myFormat.parse(myFormat.format(date));
       
       for(String strdate:dateArr)
       {
           try{
           if(flag==1 && !returnDates.equalsIgnoreCase(""))
           returnDates= returnDates+", ";
           
           Date temp =myFormat.parse(strdate);
           if(temp.after(input_date) ||temp.equals(input_date))
           returnDates = returnDates+myFormat.format(temp);
           
           flag =1;
           }
           catch(Exception e)
           {}
       }
       
       return returnDates;
        
    }

    public List<EventResult> getResults() {
        return results;
    }

    public void setResults(List<EventResult> results) {
        this.results = results;
    }

    public int getEventCount() {
        return eventCount;
    }

    public void setEventCount(int eventCount) {
        this.eventCount = eventCount;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }
    
    
    
}
