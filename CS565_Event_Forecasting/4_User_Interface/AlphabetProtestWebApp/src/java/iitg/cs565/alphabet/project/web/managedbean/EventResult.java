/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package iitg.cs565.alphabet.project.web.managedbean;

/**
 *
 * @author Neelesh
 */
public class EventResult {
    
    private int eventId;
    private String eventTitle;
    private String persons;
    private String organizations;
    private String locations;
    private String dates;
    
    public EventResult(int eventId, String eventTitle, String persons, String organizations, String locations, String dates)
    {
        this.eventId = eventId;
        this.eventTitle = eventTitle;
        this.persons = persons;
        this.organizations = organizations;
        this.locations = locations;
        this.dates = dates;
    }

    public int getEventId() {
        return eventId;
    }

    public void setEventId(int eventId) {
        this.eventId = eventId;
    }

    public String getEventTitle() {
        return eventTitle;
    }

    public void setEventTitle(String eventTitle) {
        this.eventTitle = eventTitle;
    }

    public String getPersons() {
        return persons;
    }

    public void setPersons(String persons) {
        this.persons = persons;
    }

    public String getOrganizations() {
        return organizations;
    }

    public void setOrganizations(String organizations) {
        this.organizations = organizations;
    }

    public String getLocations() {
        return locations;
    }

    public void setLocations(String locations) {
        this.locations = locations;
    }

    public String getDates() {
        return dates;
    }

    public void setDates(String dates) {
        this.dates = dates;
    }
    
    
    
}
