package Entities;


import java.util.HashMap;

/**
 * Created by juanl on 29/05/2017.
 */
public class Residence {
    private HashMap<String,FeedUser> residents = new HashMap<String,FeedUser>();
    private HashMap<String,FeedUser> guests = new HashMap<String,FeedUser>();
    private HashMap<String,FeedUser> admin = new HashMap<String,FeedUser>();
    private HashMap<String,Day> schedule = new HashMap<String,Day>();
}
