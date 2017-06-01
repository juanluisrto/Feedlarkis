package Entities;

import java.util.Date;
import java.util.HashMap;

/**
 * Created by juanl on 30/05/2017.
 */
public class Day {
    private Date date;
    private HashMap<Integer,Meal> meals = new HashMap<Integer,Meal>();
}
