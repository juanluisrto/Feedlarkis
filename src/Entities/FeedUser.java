package Entities;

/**
 * Created by juanl on 29/05/2017.
 */
import com.google.appengine.api.users.User;

import java.util.HashMap;

public class FeedUser {
    private String name;
    private String surname;
    private User gcloudUser;
    private Residence residence;
    private String role;
    private HashMap<Integer,Booking>myMeals = new HashMap<Integer,Booking>();
    private HashMap<Integer,Booking>mySpecials = new HashMap<Integer,Booking>();

    public FeedUser(String email, String authDomain, String userId, String federatedIdentity, String name, String surname, String username) {
        gcloudUser = new User(email, authDomain, userId, federatedIdentity);
        this.name = name;
        this.surname = surname;
    }


}
