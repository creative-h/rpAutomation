
<?php

ini_set('display_errors', 1);

error_reporting(E_ALL);

 

$ldap_host = "ldap://swasti.com";

$ldap_user = "swasti\\administrator";

$ldap_pass = "Shree@2029";

 

$conn = ldap_connect($ldap_host);

ldap_set_option($conn, LDAP_OPT_PROTOCOL_VERSION, 3);

ldap_set_option($conn, LDAP_OPT_REFERRALS, 0);

 

if (!ldap_bind($conn, $ldap_user, $ldap_pass)) {

    die("Bind failed: " . ldap_error($conn));

}

 

$dn = "CN=Ramesh Jain,OU=IT_DEPT,OU=swastisolutions,DC=swasti,DC=com";

 

$entry = [

    "cn" => "Ramesh Jain",

    "sn" => "Jain",

    "givenName" => "Ramesh",

    "displayName" => "Ramesh Jain",

    "sAMAccountName" => "ramesh",

    "userPrincipalName" => "ramesh@swasti.com",

    "department" => "IT_DEPT",

    "objectClass" => ["top", "person", "organizationalPerson", "user"]

];

 

$result = ldap_add($conn, $dn, $entry);

 

if ($result) {

    echo "User created successfully";

} else {

    echo "Create failed: " . ldap_error($conn);

}

 

ldap_unbind($conn);

 

 

?>