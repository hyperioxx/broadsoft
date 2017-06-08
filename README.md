discuss login fuctionality
    auto login
    doing it yourself
    passing around auth and login objects to inherit session id
    
single command (directly via object)
compound command (via attaching to BroadsoftRequest.commands)

building a new request object

broadsoftinstance
    child objects will always inherit from parent, even if set explicitly otherwise

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