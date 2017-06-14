basic usage of top level objects

provisioning a user
    build an Account object
    add Device objects to it
    run .provision()
    
    ```python3
    from broadsoft.Device import Device
    from broadsoft.Account import Account
    a = Account(use_test=True)
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
    child objects will always inherit from parent, even if set explicitly otherwise
    can pass attrs individually but not recc

passing around auth/login object/session id in Account, Device when doing big jobs to save connections

if you depend on auto login, auto logout will also happen
if you want to manage login (such as to keep session open for multiple requests), build broadsoft instance, set auto_login to False, and pass in
good form to do a logout when you're done
    
how the requestobjects work, how to create a new one
    discuss login fuctionality
        auto login
        doing it yourself
        passing around auth and login objects to inherit session id
        
    single command (directly via object)
    compound command (via attaching to BroadsoftRequest.commands)