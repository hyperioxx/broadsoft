# broadsoft

This module is used to interact with the Broadsoft OCI API.

install as a git module via:
`pip install git+ssh://git@github.mit.edu/nist/broadsoft.git@master`

**requires the following modules**
* nistcreds (```pip install git+ssh://git@github.mit.edu/braiotta/nistcreds.git@master```)

Any "common" searches should be implemented as set-it-and-forget-it, one-and-done static methods, as seen in
UserAddRequest.add().

## typical usage of XML requests

The goal of this code is to extend a requestobject for each Broadsoft XML object (eg
UserAddRequest). As noted above, each of these should extend a self-documenting static method
to simplify the use of common commands. Absent that, here's what typical usage would look
like.

The following code uses the UserAddRequest object to generate the XML necessary for that
command and post it to the Broadsoft API.

```python3
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
u_add = UserAddRequest()
u_add.first_name = 'Tim'
u_add.last_name = 'Beaver'
u_add.did = 6175551212
u_add.kname = 'beaver'
u_add.sip_user_id = 'tbeaver'
u_add.sip_password = '1234567890'
u_add.email = 'beaver@mit.edu'
u_add.post()
```


## choosing an instance

By default, the code will go to the production instance of the Broadsoft API (as seen in
broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance).

If you're using the test instance, you can pass that by constru



basic usage of top level objects

provisioning a user
    build an Account object
    add Device objects to it
    run .provision()
    
    ```python3
    from broadsoft.Device import Device
    from broadsoft.Account import Account
    a = Account(instance='test')
    a.did = 2212221100
    a.last_name = 'Braiotta'
    a.first_name = 'Chris'
    a.kname = 'braiotta'
    d1 = Device(name='braiotta 550', type='Polycom SoundPoint IP 550', description='the 550 what chris uses')
    d2 = Device(name='braiotta vvx', type='Polycom-VVX1500', description='that cool vvx')
    a.devices = [d1, d2]
    a.provision()
    ```

broadsoftinstance
    does two things:
        tracks attrs that depend on which broadsoft instance we're using (service provider id, api url)
        tracks api login info to allow persistent login
    child objects will always inherit from parent, even if set explicitly otherwise
    can pass attrs individually but not recc

passing around auth/login object/session id in Account, Device when doing big jobs to save connections

if you depend on auto login, auto logout will also happen
if you want to manage login (such as to keep session open for multiple requests), build broadsoft instance, set auto_login to False, and pass in
good form to do a logout when you're done

how to do bulk requests with atomicity (drawn from populatebroadsoft code)
    
how the requestobjects work, how to create a new one
    discuss login fuctionality
        auto login
        doing it yourself
        passing around auth and login objects to inherit session id
        
    single command (directly via object)
    compound command (via attaching to BroadsoftRequest.commands)