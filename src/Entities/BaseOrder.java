package Entities;

import java.util.Date;

/**
 * Created by juanl on 01/06/2017.
 */
public class BaseOrder {
    private int id;
    private String name;
    private String type;
    private Date time;
    private Date deadline; //Deadline to register for this meal.
    private int duration; //minutes
}
