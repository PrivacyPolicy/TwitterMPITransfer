struct Tweet {
    char* text;         // tweet
    char* user;         // username
    long int retweets;  // number of retweets
    long int favorites; // number of favorites
    float sentiment;    // between -1 and 1, sentiment of tweet
    long int id;
};
