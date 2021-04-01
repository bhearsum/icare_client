# Overview
A simple tool to fetch data from [iCareLullaboo](https://lullaboo.ca/) servers. It can fetch any of the data that the official apps can, and generate (very) simple reports.

This tool was written primarily because the official provided apps are slow, while this tool can be run periodically in the background.

# Installation
```
git clone https://github.com/bhearsum/icare_lullaboo_client icare_lullaboo_client
cd icare_lullaboo_client
python setup.py install
```

# Usage
The most common operation is generating a report. This can be done with the following commands:
```
export ICARE_USERNAME=yourusername
export ICARE_PASSWORD=yourpassword
icare report --output-format html --html-dir ~/childcare --date 03/26/2021 --child-name "Jadzia"
```

After it completes, ~/childcare/03-26-2021 will be populated with a `report.html` file, and any pictures that were available. Use your web browser to view it.

# Analysis of iCare App Traffic
This is an overview of information gleaned from a network capture from the official iCare app, with irrelevant things trimmed out.

<details>
    <summary>API request/response logs</summary>

## Login
Begins with a POST to `/fmi/data/v1/databases/iCareMobileAccess/sessions`
* Authorization header should contain HTTP Basic login (`Basic xxxxxxx` where the xxxxxxxx is the base64 encoded username and password)
* Returns a JSON response with a Bearer token located in .response.token, which will be used for future requests.
* Also returns a different access token in the `x-fm-data-access-token` header (see below)

The official app also makes a delete to `/fmi/data/v1/databases/iCareMobileAccess/sessions/xxx` where the xxx is the token from the `x-fm-data-access-token` header in the previous request. Following that it does _another_ login request. This seems like a bug, and is not replicated in this tool.

## Getting Information
From now on, all requests should contain a Authorization header with the value `Bearer xxxxxx`, where xxxxxx is the bearer token from the login request.

### Finding children associated with your account
This is the first request that is made, which will find `childID`s that will be needed for later queries.

POST to `/fmi/data/v1/databases/iCareMobileAccess/layouts/childBasicWithMobileAppUserAccountMobile/_find`, with a body like:
```
{
    "query": [{
        "mobileAppUserAccount::accountName": "my_username"
    }]
}
```

Response will look like:
```
{'messages': [{'code': '0', 'message': 'OK'}],
 'response': {'data': [{'fieldData': {'campusID': 3,
                                      'childID': 12345,
                                      'firstName': 'My',
                                      'lastName': 'Child',
                                      'middleName': '',
                                      'mobileAppUserAccount::accountName': 'my_username'},
                        'modId': '7858',
                        'portalData': {},
                        'recordId': '3279'}],
              'dataInfo': {'database': 'iCareMobileAccess',
                           'foundCount': 1,
                           'layout': 'childBasicWithMobileAppUserAccountMobile',
                           'returnedCount': 1,
                           'table': 'child',
                           'totalRecordCount': 241}}}
```

### Pictures
Notably, pictures are not stored for very long (they appear to go away around midnight?), and as such, there's no way to query by date -- it just downloads all of them every time(!).

POST request to `/fmi/data/v1/databases/iCareMobileAccess/layouts/childImageContainerMobile/_find` with a body like:
```
{
    "query": [{
        "child::childID": your_child_id
    ]}
}
```

Response will be like:
```
(fill this in when you have it)
```

### Food Information
POST request to `/fmi/data/v1/databases/iCareMobileAccess/layouts/childMealItemMobile/_find` with a body like:
```
{
    "query": [{
        "child::childID": your_child_id,
        "effectiveDate": "=03/26/2021"
    ]}
}
```

Response will look like:
```
{'messages': [{'code': '0', 'message': 'OK'}],
 'response': {'data': [{'fieldData': {'child::childID': child_id,
                                      'childEatingID': '365BE2FA-82E8-524C-A953-B7F4F2956249',
                                      'childMealItemID': 'D60F1E0C-0C0E-2047-ACE6-54269AABA68C',
                                      'effectiveDate': '03/26/2021',
                                      'meal::mealDescription': 'Snack 1',
                                      'mealID': 'DC1B68FB-AAC6-4CF9-9B8B-670B19B4DEA3',
                                      'mealResults': 'I ate well pear and 1 '
                                                     'croissant',
                                      'menu': 'Fresh Pears',
                                      'milk': 0,
                                      'milkUnits': 'cups',
                                      'roomID': 55,
                                      'water': 0,
                                      'waterUnits': 'cups'},
                        'modId': '2',
                        'portalData': {},
                        'recordId': '444151'},
                       {'fieldData': {'child::childID': child_id,
                                      'childEatingID': '365BE2FA-82E8-524C-A953-B7F4F2956249',
                                      'childMealItemID': '97F60659-85F4-3A46-9CCC-72C1C12A1619',
                                      'effectiveDate': '03/26/2021',
                                      'meal::mealDescription': 'Breakfast',
                                      'mealID': 'F3255D88-35D1-41A7-8ABF-6E65861DED64',
                                      'mealResults': 'Child drank half a milk '
                                                     'and half a banana but '
                                                     'did not eat egg. He took '
                                                     '2 bites of his toast '
                                                     'only ',
                                      'menu': 'Scrambled Eggs with Whole Wheat '
                                              'Toast',
                                      'milk': 0,
                                      'milkUnits': 'cups',
                                      'roomID': 55,
                                      'water': 0,
                                      'waterUnits': 'cups'},
                        'modId': '2',
                        'portalData': {},
                        'recordId': '444152'},
                       {'fieldData': {'child::childID': child_id,
                                      'childEatingID': '365BE2FA-82E8-524C-A953-B7F4F2956249',
                                      'childMealItemID': 'A4ABD327-887D-5341-8DD5-7ADA44FF682B',
                                      'effectiveDate': '03/26/2021',
                                      'meal::mealDescription': 'Lunch',
                                      'mealID': 'A1B30A36-5966-4DCF-B6EA-620F18F53EF1',
                                      'mealResults': 'I Ate Well only rice and '
                                                     'half a banana ',
                                      'menu': 'Spinach & Vegetable Stew with '
                                              'Brown Rice',
                                      'milk': 0.5,
                                      'milkUnits': 'cups',
                                      'roomID': 55,
                                      'water': 0,
                                      'waterUnits': 'cups'},
                        'modId': '3',
                        'portalData': {},
                        'recordId': '444153'},
                       {'fieldData': {'child::childID': child_id,
                                      'childEatingID': '365BE2FA-82E8-524C-A953-B7F4F2956249',
                                      'childMealItemID': 'D4A7710E-95C6-0546-B5A7-EC962A5AEA19',
                                      'effectiveDate': '03/26/2021',
                                      'meal::mealDescription': 'Snack 2',
                                      'mealID': '52B62BBB-E60D-4558-9C4D-4EF9D4FD0BB9',
                                      'mealResults': '',
                                      'menu': 'Roasted Honey Garlic Baby '
                                              'Carrots',
                                      'milk': 0,
                                      'milkUnits': 'cups',
                                      'roomID': 55,
                                      'water': 0,
                                      'waterUnits': 'cups'},
                        'modId': '1',
                        'portalData': {},
                        'recordId': '444154'}],
              'dataInfo': {'database': 'iCareMobileAccess',
                           'foundCount': 4,
                           'layout': 'childMealItemMobile',
                           'returnedCount': 4,
                           'table': 'childMealItem',
                           'totalRecordCount': 170612}}}
```

### Daily Activities
POST request to `/fmi/data/v1/databases/iCareMobileAccess/layouts/roomProgramDailyActivityMobile/_find` with a body like:
```
{'query': [{'childAttendanceRoomProgramDailyActivity::childID': your_child_id,
            'childEating::childID': your_child_id,
            'effectiveDate': '03/26/2021'}]}
```

Sample response:
```
{'messages': [{'code': '0', 'message': 'OK'}],
 'response': {'data': [{'fieldData': {'effectiveDate': '03/26/2021',
                                      'programTaskArea::name': 'Arts',
                                      'programTaskAreaID': '0725AF46-43EC-4D8B-BB0C-D84C29A64A30',
                                      'roomID': 55,
                                      'roomProgram::interestTopic': 'days of '
                                                                    'the week',
                                      'roomProgram::parentsParticipate': '',
                                      'roomProgram::wordOfTheWeek': 'Friday',
                                      'roomProgramDailyActivityID': '3B25CDDD-D4F7-6D44-AFA4-02F2C63137BE',
                                      'roomProgramElectGoal::goal': '5.03 Fine '
                                                                    'Motor '
                                                                    'Skills',
                                      'roomProgramID': '1078C355-140E-9641-BC80-72B888E44E2E',
                                      'roomProgramTaskAreaID': 'B97A5EA5-2808-FE4F-9D27-844825AED58A',
                                      'task': "let's decorate your Friday with "
                                              'the color ful materials '},
                        'modId': '0',
                        'portalData': {'childAttendanceRoomProgramDailyActivity': [{'childAttendanceRoomProgramDailyActivity::childID': 11100,
                                                                                    'modId': '3',
                                                                                    'recordId': '165472'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11025,
                                                                                    'modId': '2',
                                                                                    'recordId': '165474'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11143,
                                                                                    'modId': '2',
                                                                                    'recordId': '165476'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11109,
                                                                                    'modId': '3',
                                                                                    'recordId': '165478'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': child_id,
                                                                                    'modId': '3',
                                                                                    'recordId': '165485'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10809,
                                                                                    'modId': '3',
                                                                                    'recordId': '165488'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11020,
                                                                                    'modId': '3',
                                                                                    'recordId': '165489'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10994,
                                                                                    'modId': '2',
                                                                                    'recordId': '165494'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11043,
                                                                                    'modId': '2',
                                                                                    'recordId': '165498'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11028,
                                                                                    'modId': '2',
                                                                                    'recordId': '165499'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11014,
                                                                                    'modId': '3',
                                                                                    'recordId': '165501'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11099,
                                                                                    'modId': '3',
                                                                                    'recordId': '165506'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11133,
                                                                                    'modId': '2',
                                                                                    'recordId': '165509'}],
                                       'childEating': [{'childEating::childID': child_id,
                                                        'childEating::comments': 'Preschool '
                                                                                 '1 '
                                                                                 'today '
                                                                                 'enjoyed '
                                                                                 'an '
                                                                                 'art '
                                                                                 'session '
                                                                                 'painting '
                                                                                 'spring '
                                                                                 'colors '
                                                                                 'and '
                                                                                 'mixing '
                                                                                 'them '
                                                                                 'to '
                                                                                 'obtain '
                                                                                 'different '
                                                                                 'colors '
                                                                                 'on '
                                                                                 'different '
                                                                                 'textures. '
                                                                                 'Some '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'on '
                                                                                 'papers, '
                                                                                 'others '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'their '
                                                                                 'paper '
                                                                                 'plates '
                                                                                 'and '
                                                                                 'some '
                                                                                 'used '
                                                                                 'the '
                                                                                 'popsicle '
                                                                                 'sticks '
                                                                                 'to '
                                                                                 'color '
                                                                                 'it '
                                                                                 'while '
                                                                                 'others '
                                                                                 'colored '
                                                                                 'the '
                                                                                 'aluminum '
                                                                                 'foil. '
                                                                                 'It '
                                                                                 'was '
                                                                                 'nice '
                                                                                 'to '
                                                                                 'experience '
                                                                                 'the '
                                                                                 'different '
                                                                                 'textures '
                                                                                 'we '
                                                                                 'had '
                                                                                 'while '
                                                                                 'painting. '
                                                                                 'For '
                                                                                 'circle '
                                                                                 'time '
                                                                                 'today '
                                                                                 'we '
                                                                                 'sat '
                                                                                 'around '
                                                                                 'the '
                                                                                 'table '
                                                                                 'and '
                                                                                 'spoke '
                                                                                 'about '
                                                                                 'letter '
                                                                                 'F '
                                                                                 'and '
                                                                                 "today's "
                                                                                 'Friday. '
                                                                                 'We '
                                                                                 'repeated '
                                                                                 'happy '
                                                                                 'Friday '
                                                                                 'and '
                                                                                 'we '
                                                                                 'cheered '
                                                                                 'then '
                                                                                 'we '
                                                                                 'used '
                                                                                 'markers '
                                                                                 'to '
                                                                                 'try '
                                                                                 'and '
                                                                                 'trace '
                                                                                 'the '
                                                                                 'letter '
                                                                                 'F. '
                                                                                 'We '
                                                                                 'also '
                                                                                 'learnt '
                                                                                 'about '
                                                                                 'shapes '
                                                                                 'were '
                                                                                 'we '
                                                                                 'had '
                                                                                 'a '
                                                                                 'coloring '
                                                                                 'station '
                                                                                 'with '
                                                                                 'crayons '
                                                                                 'with '
                                                                                 'different '
                                                                                 'shapes. \r'
                                                                                 '\r'
                                                                                 'Next '
                                                                                 'Thursday '
                                                                                 'we '
                                                                                 'would '
                                                                                 'like '
                                                                                 'to '
                                                                                 'see '
                                                                                 'our '
                                                                                 'kids '
                                                                                 'in '
                                                                                 'a '
                                                                                 'crazy '
                                                                                 'hat '
                                                                                 'day. '
                                                                                 'Be '
                                                                                 'creative '
                                                                                 'parents '
                                                                                 ':) \r'
                                                                                 '\r'
                                                                                 'We '
                                                                                 'wish '
                                                                                 'you '
                                                                                 'a '
                                                                                 'safe '
                                                                                 'weekend '
                                                                                 'and '
                                                                                 'see '
                                                                                 'you '
                                                                                 'next '
                                                                                 'week. ',
                                                        'modId': '2',
                                                        'recordId': '115570'}]},
                        'portalDataInfo': [{'database': 'iCareData',
                                            'foundCount': 1,
                                            'returnedCount': 1,
                                            'table': 'childEating'},
                                           {'database': 'iCareData',
                                            'foundCount': 13,
                                            'returnedCount': 13,
                                            'table': 'childAttendanceRoomProgramDailyActivity'}],
                        'recordId': '118192'},
                       {'fieldData': {'effectiveDate': '03/26/2021',
                                      'programTaskArea::name': 'Language',
                                      'programTaskAreaID': '7A977F1F-7281-48E3-937E-C777E97A8110',
                                      'roomID': 55,
                                      'roomProgram::interestTopic': 'days of '
                                                                    'the week',
                                      'roomProgram::parentsParticipate': '',
                                      'roomProgram::wordOfTheWeek': 'Friday',
                                      'roomProgramDailyActivityID': '6DBA958B-2CA0-9641-9A45-AE05DAAAFE7A',
                                      'roomProgramElectGoal::goal': '5.03 Fine '
                                                                    'Motor '
                                                                    'Skills',
                                      'roomProgramID': '1078C355-140E-9641-BC80-72B888E44E2E',
                                      'roomProgramTaskAreaID': '2A0A59C0-ACB3-EE46-82E7-81D64040F354',
                                      'task': "let's find the letters which "
                                              'was hidden in the papers'},
                        'modId': '0',
                        'portalData': {'childAttendanceRoomProgramDailyActivity': [{'childAttendanceRoomProgramDailyActivity::childID': 11100,
                                                                                    'modId': '3',
                                                                                    'recordId': '165472'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11025,
                                                                                    'modId': '2',
                                                                                    'recordId': '165474'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11143,
                                                                                    'modId': '2',
                                                                                    'recordId': '165476'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11109,
                                                                                    'modId': '3',
                                                                                    'recordId': '165478'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': child_id,
                                                                                    'modId': '3',
                                                                                    'recordId': '165485'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10809,
                                                                                    'modId': '3',
                                                                                    'recordId': '165488'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11020,
                                                                                    'modId': '3',
                                                                                    'recordId': '165489'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10994,
                                                                                    'modId': '2',
                                                                                    'recordId': '165494'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11043,
                                                                                    'modId': '2',
                                                                                    'recordId': '165498'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11028,
                                                                                    'modId': '2',
                                                                                    'recordId': '165499'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11014,
                                                                                    'modId': '3',
                                                                                    'recordId': '165501'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11099,
                                                                                    'modId': '3',
                                                                                    'recordId': '165506'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11133,
                                                                                    'modId': '2',
                                                                                    'recordId': '165509'}],
                                       'childEating': [{'childEating::childID': child_id,
                                                        'childEating::comments': 'Preschool '
                                                                                 '1 '
                                                                                 'today '
                                                                                 'enjoyed '
                                                                                 'an '
                                                                                 'art '
                                                                                 'session '
                                                                                 'painting '
                                                                                 'spring '
                                                                                 'colors '
                                                                                 'and '
                                                                                 'mixing '
                                                                                 'them '
                                                                                 'to '
                                                                                 'obtain '
                                                                                 'different '
                                                                                 'colors '
                                                                                 'on '
                                                                                 'different '
                                                                                 'textures. '
                                                                                 'Some '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'on '
                                                                                 'papers, '
                                                                                 'others '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'their '
                                                                                 'paper '
                                                                                 'plates '
                                                                                 'and '
                                                                                 'some '
                                                                                 'used '
                                                                                 'the '
                                                                                 'popsicle '
                                                                                 'sticks '
                                                                                 'to '
                                                                                 'color '
                                                                                 'it '
                                                                                 'while '
                                                                                 'others '
                                                                                 'colored '
                                                                                 'the '
                                                                                 'aluminum '
                                                                                 'foil. '
                                                                                 'It '
                                                                                 'was '
                                                                                 'nice '
                                                                                 'to '
                                                                                 'experience '
                                                                                 'the '
                                                                                 'different '
                                                                                 'textures '
                                                                                 'we '
                                                                                 'had '
                                                                                 'while '
                                                                                 'painting. '
                                                                                 'For '
                                                                                 'circle '
                                                                                 'time '
                                                                                 'today '
                                                                                 'we '
                                                                                 'sat '
                                                                                 'around '
                                                                                 'the '
                                                                                 'table '
                                                                                 'and '
                                                                                 'spoke '
                                                                                 'about '
                                                                                 'letter '
                                                                                 'F '
                                                                                 'and '
                                                                                 "today's "
                                                                                 'Friday. '
                                                                                 'We '
                                                                                 'repeated '
                                                                                 'happy '
                                                                                 'Friday '
                                                                                 'and '
                                                                                 'we '
                                                                                 'cheered '
                                                                                 'then '
                                                                                 'we '
                                                                                 'used '
                                                                                 'markers '
                                                                                 'to '
                                                                                 'try '
                                                                                 'and '
                                                                                 'trace '
                                                                                 'the '
                                                                                 'letter '
                                                                                 'F. '
                                                                                 'We '
                                                                                 'also '
                                                                                 'learnt '
                                                                                 'about '
                                                                                 'shapes '
                                                                                 'were '
                                                                                 'we '
                                                                                 'had '
                                                                                 'a '
                                                                                 'coloring '
                                                                                 'station '
                                                                                 'with '
                                                                                 'crayons '
                                                                                 'with '
                                                                                 'different '
                                                                                 'shapes. \r'
                                                                                 '\r'
                                                                                 'Next '
                                                                                 'Thursday '
                                                                                 'we '
                                                                                 'would '
                                                                                 'like '
                                                                                 'to '
                                                                                 'see '
                                                                                 'our '
                                                                                 'kids '
                                                                                 'in '
                                                                                 'a '
                                                                                 'crazy '
                                                                                 'hat '
                                                                                 'day. '
                                                                                 'Be '
                                                                                 'creative '
                                                                                 'parents '
                                                                                 ':) \r'
                                                                                 '\r'
                                                                                 'We '
                                                                                 'wish '
                                                                                 'you '
                                                                                 'a '
                                                                                 'safe '
                                                                                 'weekend '
                                                                                 'and '
                                                                                 'see '
                                                                                 'you '
                                                                                 'next '
                                                                                 'week. ',
                                                        'modId': '2',
                                                        'recordId': '115570'}]},
                        'portalDataInfo': [{'database': 'iCareData',
                                            'foundCount': 1,
                                            'returnedCount': 1,
                                            'table': 'childEating'},
                                           {'database': 'iCareData',
                                            'foundCount': 13,
                                            'returnedCount': 13,
                                            'table': 'childAttendanceRoomProgramDailyActivity'}],
                        'recordId': '118193'},
                       {'fieldData': {'effectiveDate': '03/26/2021',
                                      'programTaskArea::name': 'Math',
                                      'programTaskAreaID': '8506F795-6FFF-4EB6-A7DE-94E95C31436B',
                                      'roomID': 55,
                                      'roomProgram::interestTopic': 'days of '
                                                                    'the week',
                                      'roomProgram::parentsParticipate': '',
                                      'roomProgram::wordOfTheWeek': 'Friday',
                                      'roomProgramDailyActivityID': 'AF7D4069-1536-FD46-8F0E-CF078E8E1225',
                                      'roomProgramElectGoal::goal': '5.03 Fine '
                                                                    'Motor '
                                                                    'Skills',
                                      'roomProgramID': '1078C355-140E-9641-BC80-72B888E44E2E',
                                      'roomProgramTaskAreaID': '4279CAE8-BD2A-EB49-86D4-0E3C061AA300',
                                      'task': "let's match the body parts by "
                                              'using glue '},
                        'modId': '0',
                        'portalData': {'childAttendanceRoomProgramDailyActivity': [{'childAttendanceRoomProgramDailyActivity::childID': 11100,
                                                                                    'modId': '3',
                                                                                    'recordId': '165472'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11025,
                                                                                    'modId': '2',
                                                                                    'recordId': '165474'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11143,
                                                                                    'modId': '2',
                                                                                    'recordId': '165476'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11109,
                                                                                    'modId': '3',
                                                                                    'recordId': '165478'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': child_id,
                                                                                    'modId': '3',
                                                                                    'recordId': '165485'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10809,
                                                                                    'modId': '3',
                                                                                    'recordId': '165488'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11020,
                                                                                    'modId': '3',
                                                                                    'recordId': '165489'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10994,
                                                                                    'modId': '2',
                                                                                    'recordId': '165494'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11043,
                                                                                    'modId': '2',
                                                                                    'recordId': '165498'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11028,
                                                                                    'modId': '2',
                                                                                    'recordId': '165499'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11014,
                                                                                    'modId': '3',
                                                                                    'recordId': '165501'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11099,
                                                                                    'modId': '3',
                                                                                    'recordId': '165506'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11133,
                                                                                    'modId': '2',
                                                                                    'recordId': '165509'}],
                                       'childEating': [{'childEating::childID': child_id,
                                                        'childEating::comments': 'Preschool '
                                                                                 '1 '
                                                                                 'today '
                                                                                 'enjoyed '
                                                                                 'an '
                                                                                 'art '
                                                                                 'session '
                                                                                 'painting '
                                                                                 'spring '
                                                                                 'colors '
                                                                                 'and '
                                                                                 'mixing '
                                                                                 'them '
                                                                                 'to '
                                                                                 'obtain '
                                                                                 'different '
                                                                                 'colors '
                                                                                 'on '
                                                                                 'different '
                                                                                 'textures. '
                                                                                 'Some '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'on '
                                                                                 'papers, '
                                                                                 'others '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'their '
                                                                                 'paper '
                                                                                 'plates '
                                                                                 'and '
                                                                                 'some '
                                                                                 'used '
                                                                                 'the '
                                                                                 'popsicle '
                                                                                 'sticks '
                                                                                 'to '
                                                                                 'color '
                                                                                 'it '
                                                                                 'while '
                                                                                 'others '
                                                                                 'colored '
                                                                                 'the '
                                                                                 'aluminum '
                                                                                 'foil. '
                                                                                 'It '
                                                                                 'was '
                                                                                 'nice '
                                                                                 'to '
                                                                                 'experience '
                                                                                 'the '
                                                                                 'different '
                                                                                 'textures '
                                                                                 'we '
                                                                                 'had '
                                                                                 'while '
                                                                                 'painting. '
                                                                                 'For '
                                                                                 'circle '
                                                                                 'time '
                                                                                 'today '
                                                                                 'we '
                                                                                 'sat '
                                                                                 'around '
                                                                                 'the '
                                                                                 'table '
                                                                                 'and '
                                                                                 'spoke '
                                                                                 'about '
                                                                                 'letter '
                                                                                 'F '
                                                                                 'and '
                                                                                 "today's "
                                                                                 'Friday. '
                                                                                 'We '
                                                                                 'repeated '
                                                                                 'happy '
                                                                                 'Friday '
                                                                                 'and '
                                                                                 'we '
                                                                                 'cheered '
                                                                                 'then '
                                                                                 'we '
                                                                                 'used '
                                                                                 'markers '
                                                                                 'to '
                                                                                 'try '
                                                                                 'and '
                                                                                 'trace '
                                                                                 'the '
                                                                                 'letter '
                                                                                 'F. '
                                                                                 'We '
                                                                                 'also '
                                                                                 'learnt '
                                                                                 'about '
                                                                                 'shapes '
                                                                                 'were '
                                                                                 'we '
                                                                                 'had '
                                                                                 'a '
                                                                                 'coloring '
                                                                                 'station '
                                                                                 'with '
                                                                                 'crayons '
                                                                                 'with '
                                                                                 'different '
                                                                                 'shapes. \r'
                                                                                 '\r'
                                                                                 'Next '
                                                                                 'Thursday '
                                                                                 'we '
                                                                                 'would '
                                                                                 'like '
                                                                                 'to '
                                                                                 'see '
                                                                                 'our '
                                                                                 'kids '
                                                                                 'in '
                                                                                 'a '
                                                                                 'crazy '
                                                                                 'hat '
                                                                                 'day. '
                                                                                 'Be '
                                                                                 'creative '
                                                                                 'parents '
                                                                                 ':) \r'
                                                                                 '\r'
                                                                                 'We '
                                                                                 'wish '
                                                                                 'you '
                                                                                 'a '
                                                                                 'safe '
                                                                                 'weekend '
                                                                                 'and '
                                                                                 'see '
                                                                                 'you '
                                                                                 'next '
                                                                                 'week. ',
                                                        'modId': '2',
                                                        'recordId': '115570'}]},
                        'portalDataInfo': [{'database': 'iCareData',
                                            'foundCount': 1,
                                            'returnedCount': 1,
                                            'table': 'childEating'},
                                           {'database': 'iCareData',
                                            'foundCount': 13,
                                            'returnedCount': 13,
                                            'table': 'childAttendanceRoomProgramDailyActivity'}],
                        'recordId': '118194'},
                       {'fieldData': {'effectiveDate': '03/26/2021',
                                      'programTaskArea::name': 'Science',
                                      'programTaskAreaID': 'D53606E3-4D59-4EBE-9754-5613DF5B76D9',
                                      'roomID': 55,
                                      'roomProgram::interestTopic': 'days of '
                                                                    'the week',
                                      'roomProgram::parentsParticipate': '',
                                      'roomProgram::wordOfTheWeek': 'Friday',
                                      'roomProgramDailyActivityID': '1C12518F-95B8-1F46-9D80-F7B9A3ADB8D3',
                                      'roomProgramElectGoal::goal': '5.03 Fine '
                                                                    'Motor '
                                                                    'Skills',
                                      'roomProgramID': '1078C355-140E-9641-BC80-72B888E44E2E',
                                      'roomProgramTaskAreaID': 'A22F69A0-45FE-9248-B6DE-DE156E58F924',
                                      'task': "let's play the bottle of the "
                                              'water mixed with the oil '},
                        'modId': '0',
                        'portalData': {'childAttendanceRoomProgramDailyActivity': [{'childAttendanceRoomProgramDailyActivity::childID': 11100,
                                                                                    'modId': '3',
                                                                                    'recordId': '165472'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11025,
                                                                                    'modId': '2',
                                                                                    'recordId': '165474'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11143,
                                                                                    'modId': '2',
                                                                                    'recordId': '165476'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11109,
                                                                                    'modId': '3',
                                                                                    'recordId': '165478'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': child_id,
                                                                                    'modId': '3',
                                                                                    'recordId': '165485'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10809,
                                                                                    'modId': '3',
                                                                                    'recordId': '165488'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11020,
                                                                                    'modId': '3',
                                                                                    'recordId': '165489'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10994,
                                                                                    'modId': '2',
                                                                                    'recordId': '165494'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11043,
                                                                                    'modId': '2',
                                                                                    'recordId': '165498'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11028,
                                                                                    'modId': '2',
                                                                                    'recordId': '165499'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11014,
                                                                                    'modId': '3',
                                                                                    'recordId': '165501'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11099,
                                                                                    'modId': '3',
                                                                                    'recordId': '165506'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11133,
                                                                                    'modId': '2',
                                                                                    'recordId': '165509'}],
                                       'childEating': [{'childEating::childID': child_id,
                                                        'childEating::comments': 'Preschool '
                                                                                 '1 '
                                                                                 'today '
                                                                                 'enjoyed '
                                                                                 'an '
                                                                                 'art '
                                                                                 'session '
                                                                                 'painting '
                                                                                 'spring '
                                                                                 'colors '
                                                                                 'and '
                                                                                 'mixing '
                                                                                 'them '
                                                                                 'to '
                                                                                 'obtain '
                                                                                 'different '
                                                                                 'colors '
                                                                                 'on '
                                                                                 'different '
                                                                                 'textures. '
                                                                                 'Some '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'on '
                                                                                 'papers, '
                                                                                 'others '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'their '
                                                                                 'paper '
                                                                                 'plates '
                                                                                 'and '
                                                                                 'some '
                                                                                 'used '
                                                                                 'the '
                                                                                 'popsicle '
                                                                                 'sticks '
                                                                                 'to '
                                                                                 'color '
                                                                                 'it '
                                                                                 'while '
                                                                                 'others '
                                                                                 'colored '
                                                                                 'the '
                                                                                 'aluminum '
                                                                                 'foil. '
                                                                                 'It '
                                                                                 'was '
                                                                                 'nice '
                                                                                 'to '
                                                                                 'experience '
                                                                                 'the '
                                                                                 'different '
                                                                                 'textures '
                                                                                 'we '
                                                                                 'had '
                                                                                 'while '
                                                                                 'painting. '
                                                                                 'For '
                                                                                 'circle '
                                                                                 'time '
                                                                                 'today '
                                                                                 'we '
                                                                                 'sat '
                                                                                 'around '
                                                                                 'the '
                                                                                 'table '
                                                                                 'and '
                                                                                 'spoke '
                                                                                 'about '
                                                                                 'letter '
                                                                                 'F '
                                                                                 'and '
                                                                                 "today's "
                                                                                 'Friday. '
                                                                                 'We '
                                                                                 'repeated '
                                                                                 'happy '
                                                                                 'Friday '
                                                                                 'and '
                                                                                 'we '
                                                                                 'cheered '
                                                                                 'then '
                                                                                 'we '
                                                                                 'used '
                                                                                 'markers '
                                                                                 'to '
                                                                                 'try '
                                                                                 'and '
                                                                                 'trace '
                                                                                 'the '
                                                                                 'letter '
                                                                                 'F. '
                                                                                 'We '
                                                                                 'also '
                                                                                 'learnt '
                                                                                 'about '
                                                                                 'shapes '
                                                                                 'were '
                                                                                 'we '
                                                                                 'had '
                                                                                 'a '
                                                                                 'coloring '
                                                                                 'station '
                                                                                 'with '
                                                                                 'crayons '
                                                                                 'with '
                                                                                 'different '
                                                                                 'shapes. \r'
                                                                                 '\r'
                                                                                 'Next '
                                                                                 'Thursday '
                                                                                 'we '
                                                                                 'would '
                                                                                 'like '
                                                                                 'to '
                                                                                 'see '
                                                                                 'our '
                                                                                 'kids '
                                                                                 'in '
                                                                                 'a '
                                                                                 'crazy '
                                                                                 'hat '
                                                                                 'day. '
                                                                                 'Be '
                                                                                 'creative '
                                                                                 'parents '
                                                                                 ':) \r'
                                                                                 '\r'
                                                                                 'We '
                                                                                 'wish '
                                                                                 'you '
                                                                                 'a '
                                                                                 'safe '
                                                                                 'weekend '
                                                                                 'and '
                                                                                 'see '
                                                                                 'you '
                                                                                 'next '
                                                                                 'week. ',
                                                        'modId': '2',
                                                        'recordId': '115570'}]},
                        'portalDataInfo': [{'database': 'iCareData',
                                            'foundCount': 1,
                                            'returnedCount': 1,
                                            'table': 'childEating'},
                                           {'database': 'iCareData',
                                            'foundCount': 13,
                                            'returnedCount': 13,
                                            'table': 'childAttendanceRoomProgramDailyActivity'}],
                        'recordId': '118196'},
                       {'fieldData': {'effectiveDate': '03/26/2021',
                                      'programTaskArea::name': 'Whole Group '
                                                               'Learning',
                                      'programTaskAreaID': '3A9D1D14-8C3C-462A-922A-D952C612F4CA',
                                      'roomID': 55,
                                      'roomProgram::interestTopic': 'days of '
                                                                    'the week',
                                      'roomProgram::parentsParticipate': '',
                                      'roomProgram::wordOfTheWeek': 'Friday',
                                      'roomProgramDailyActivityID': 'F6B298B5-6701-FB4E-A494-805FDAE53C2D',
                                      'roomProgramElectGoal::goal': '5.03 Fine '
                                                                    'Motor '
                                                                    'Skills',
                                      'roomProgramID': '1078C355-140E-9641-BC80-72B888E44E2E',
                                      'roomProgramTaskAreaID': '21E07F51-D47A-7645-9B14-50F25418F57F',
                                      'task': "let's practice our physical "
                                              'skills to walk by the feet '
                                              'prints'},
                        'modId': '0',
                        'portalData': {'childAttendanceRoomProgramDailyActivity': [{'childAttendanceRoomProgramDailyActivity::childID': 11100,
                                                                                    'modId': '3',
                                                                                    'recordId': '165472'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11025,
                                                                                    'modId': '2',
                                                                                    'recordId': '165474'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11143,
                                                                                    'modId': '2',
                                                                                    'recordId': '165476'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11109,
                                                                                    'modId': '3',
                                                                                    'recordId': '165478'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': child_id,
                                                                                    'modId': '3',
                                                                                    'recordId': '165485'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10809,
                                                                                    'modId': '3',
                                                                                    'recordId': '165488'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11020,
                                                                                    'modId': '3',
                                                                                    'recordId': '165489'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 10994,
                                                                                    'modId': '2',
                                                                                    'recordId': '165494'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11043,
                                                                                    'modId': '2',
                                                                                    'recordId': '165498'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11028,
                                                                                    'modId': '2',
                                                                                    'recordId': '165499'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11014,
                                                                                    'modId': '3',
                                                                                    'recordId': '165501'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11099,
                                                                                    'modId': '3',
                                                                                    'recordId': '165506'},
                                                                                   {'childAttendanceRoomProgramDailyActivity::childID': 11133,
                                                                                    'modId': '2',
                                                                                    'recordId': '165509'}],
                                       'childEating': [{'childEating::childID': child_id,
                                                        'childEating::comments': 'Preschool '
                                                                                 '1 '
                                                                                 'today '
                                                                                 'enjoyed '
                                                                                 'an '
                                                                                 'art '
                                                                                 'session '
                                                                                 'painting '
                                                                                 'spring '
                                                                                 'colors '
                                                                                 'and '
                                                                                 'mixing '
                                                                                 'them '
                                                                                 'to '
                                                                                 'obtain '
                                                                                 'different '
                                                                                 'colors '
                                                                                 'on '
                                                                                 'different '
                                                                                 'textures. '
                                                                                 'Some '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'on '
                                                                                 'papers, '
                                                                                 'others '
                                                                                 'wanted '
                                                                                 'to '
                                                                                 'paint '
                                                                                 'their '
                                                                                 'paper '
                                                                                 'plates '
                                                                                 'and '
                                                                                 'some '
                                                                                 'used '
                                                                                 'the '
                                                                                 'popsicle '
                                                                                 'sticks '
                                                                                 'to '
                                                                                 'color '
                                                                                 'it '
                                                                                 'while '
                                                                                 'others '
                                                                                 'colored '
                                                                                 'the '
                                                                                 'aluminum '
                                                                                 'foil. '
                                                                                 'It '
                                                                                 'was '
                                                                                 'nice '
                                                                                 'to '
                                                                                 'experience '
                                                                                 'the '
                                                                                 'different '
                                                                                 'textures '
                                                                                 'we '
                                                                                 'had '
                                                                                 'while '
                                                                                 'painting. '
                                                                                 'For '
                                                                                 'circle '
                                                                                 'time '
                                                                                 'today '
                                                                                 'we '
                                                                                 'sat '
                                                                                 'around '
                                                                                 'the '
                                                                                 'table '
                                                                                 'and '
                                                                                 'spoke '
                                                                                 'about '
                                                                                 'letter '
                                                                                 'F '
                                                                                 'and '
                                                                                 "today's "
                                                                                 'Friday. '
                                                                                 'We '
                                                                                 'repeated '
                                                                                 'happy '
                                                                                 'Friday '
                                                                                 'and '
                                                                                 'we '
                                                                                 'cheered '
                                                                                 'then '
                                                                                 'we '
                                                                                 'used '
                                                                                 'markers '
                                                                                 'to '
                                                                                 'try '
                                                                                 'and '
                                                                                 'trace '
                                                                                 'the '
                                                                                 'letter '
                                                                                 'F. '
                                                                                 'We '
                                                                                 'also '
                                                                                 'learnt '
                                                                                 'about '
                                                                                 'shapes '
                                                                                 'were '
                                                                                 'we '
                                                                                 'had '
                                                                                 'a '
                                                                                 'coloring '
                                                                                 'station '
                                                                                 'with '
                                                                                 'crayons '
                                                                                 'with '
                                                                                 'different '
                                                                                 'shapes. \r'
                                                                                 '\r'
                                                                                 'Next '
                                                                                 'Thursday '
                                                                                 'we '
                                                                                 'would '
                                                                                 'like '
                                                                                 'to '
                                                                                 'see '
                                                                                 'our '
                                                                                 'kids '
                                                                                 'in '
                                                                                 'a '
                                                                                 'crazy '
                                                                                 'hat '
                                                                                 'day. '
                                                                                 'Be '
                                                                                 'creative '
                                                                                 'parents '
                                                                                 ':) \r'
                                                                                 '\r'
                                                                                 'We '
                                                                                 'wish '
                                                                                 'you '
                                                                                 'a '
                                                                                 'safe '
                                                                                 'weekend '
                                                                                 'and '
                                                                                 'see '
                                                                                 'you '
                                                                                 'next '
                                                                                 'week. ',
                                                        'modId': '2',
                                                        'recordId': '115570'}]},
                        'portalDataInfo': [{'database': 'iCareData',
                                            'foundCount': 1,
                                            'returnedCount': 1,
                                            'table': 'childEating'},
                                           {'database': 'iCareData',
                                            'foundCount': 13,
                                            'returnedCount': 13,
                                            'table': 'childAttendanceRoomProgramDailyActivity'}],
                        'recordId': '118197'}],
              'dataInfo': {'database': 'iCareMobileAccess',
                           'foundCount': 5,
                           'layout': 'roomProgramDailyActivityMobile',
                           'returnedCount': 5,
                           'table': 'roomProgramDailyActivity',
                           'totalRecordCount': 57595}}}
```

### Diaper/Potty Information
POST request to /fmi/data/v1/databases/iCareMobileAccess/layouts/childDiaperMobile/_find with a body like:
```
{
    'query': [{
        'child::childId': child_id,
        'dateChanged': '=03/26/2021'
    }]
}
```

Returns a body like:
```
{'messages': [{'code': '0', 'message': 'OK'}],
 'response': {'data': [{'fieldData': {'child::childID': child_id,
                                      'childDiaperID': 'D22120B8-8413-F34F-87CA-6DE5C8584344',
                                      'creamApplied': '',
                                      'creamType': '',
                                      'dateChanged': '03/26/2021',
                                      'timeChanged': '09:24:59',
                                      'timestampChanged': '03/26/2021 09:24:59',
                                      'wetOrBM': 'Urinated in Toilet'},
                        'modId': '0',
                        'portalData': {},
                        'recordId': '424000'},
                       {'fieldData': {'child::childID': child_id,
                                      'childDiaperID': '1A4590A3-CB6E-4845-AA92-4861E1216DD9',
                                      'creamApplied': '',
                                      'creamType': '',
                                      'dateChanged': '03/26/2021',
                                      'timeChanged': '12:01:00',
                                      'timestampChanged': '03/26/2021 12:01:00',
                                      'wetOrBM': 'Urinated in Toilet'},
                        'modId': '1',
                        'portalData': {},
                        'recordId': '424062'},
                       {'fieldData': {'child::childID': child_id,
                                      'childDiaperID': 'FC5E8E98-F61D-974F-8C5D-FCACB94EF3A5',
                                      'creamApplied': '',
                                      'creamType': '',
                                      'dateChanged': '03/26/2021',
                                      'timeChanged': '13:50:52',
                                      'timestampChanged': '03/26/2021 13:50:52',
                                      'wetOrBM': 'Urinated in Toilet'},
                        'modId': '0',
                        'portalData': {},
                        'recordId': '424083'},
                       {'fieldData': {'child::childID': child_id,
                                      'childDiaperID': '0ECFF7DF-5066-A246-930E-92F555073382',
                                      'creamApplied': '',
                                      'creamType': '',
                                      'dateChanged': '03/26/2021',
                                      'timeChanged': '16:21:57',
                                      'timestampChanged': '03/26/2021 16:21:57',
                                      'wetOrBM': 'Urinated in Toilet'},
                        'modId': '0',
                        'portalData': {},
                        'recordId': '424138'}],
              'dataInfo': {'database': 'iCareMobileAccess',
                           'foundCount': 4,
                           'layout': 'childDiaperMobile',
                           'returnedCount': 4,
                           'table': 'childDiaper',
                           'totalRecordCount': 153741}}}

### Nap Information
POST request to `/fmi/data/v1/databases/iCareMobileAccess/layouts/childSleepMobile/_find` with a body like:
```
{
    'query': [{
        'child::childId': child_id, 'sleepDate': '=03/26/2021'
    }]
}
```

Returns a body like:
```
{'messages': [{'code': '0', 'message': 'OK'}],
 'response': {'data': [{'fieldData': {'child::childID': child_id,
    
                                      'childSleepID': '0209B039-C7DC-4D76-BC42-050884B437CD',
                                      'commentOnly': '',
                                      'comments': 'Normal sleeping pattern',
                                      'createTS': '03/26/2021 12:12:11',
                                      'nameFirstLast': 'Child Name',
                                      'roomChildSleep::name': 'Preschool 1',
                                      'roomID': 55,
                                      'sleepDate': '03/26/2021',
                                      'sleepDuration': '01:31:08',
                                      'sleepTimestamp': '03/26/2021 12:12:12',
                                      'wakeTimestamp': '03/26/2021 13:43:20'},
                        'modId': '2',
                        'portalData': {},
                        'recordId': '127073'},
                       {'fieldData': {'child::childID': child_id,
                                      'childSleepID': '2A20369C-9B2D-DD48-9946-E2CEBECA013F',
                                      'commentOnly': '',
                                      'comments': '',
                                      'createTS': '03/26/2021 13:50:41',
                                      'nameFirstLast': 'Child Name',
                                      'roomChildSleep::name': 'Preschool 1',
                                      'roomID': 55,
                                      'sleepDate': '03/26/2021',
                                      'sleepDuration': '00:00:02',
                                      'sleepTimestamp': '03/26/2021 13:50:41',
                                      'wakeTimestamp': '03/26/2021 13:50:43'},
                        'modId': '1',
                        'portalData': {},
                        'recordId': '127107'}],
              'dataInfo': {'database': 'iCareMobileAccess',
                           'foundCount': 2,
                           'layout': 'childSleepMobile',
                           'returnedCount': 2,
                           'table': 'childSleep',
                           'totalRecordCount': 45318}}}
```

### Requested Items
(This contains things that they daycare is requesting you bring, eg: diapers, blanket, etc.)

POST request to `/fmi/data/v1/databases/iCareMobileAccess/layouts/childItemRequestMobile/_find` with a body like:
```
{
    'query': [{
        'child::childId': child_id,
        'requestDate': '=03/26/2021'
    }]
}
```

Returns a body like:
```
(insert here when you have an example)
```

### Special Interests
This returns some freeform text that the daycare can put any information they want in. (Despite the layout below being called `ChildEatingMobile`, this is not a typo.)

POST request to `/fmi/data/v1/databases/iCareMobileAccess/layouts/ChildEatingMobile/_find` with a body like:
```
{
    'query': [{
        'child::childID': child_id,
        'effectiveDate': '03/26/2021'
    }]
}
```

</details>
