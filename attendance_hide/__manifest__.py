


{
    'name': "Customization of attendance",
    'summary': """
  	kiosk mode only visible for the user	
  	""",
    'description': """
       kiosk mode only visible for the user""",
    'version': "13.0.1.0.0",
    'license': 'AGPL-3',
    'depends': [
        'base','hr_attendance'
    ],
    'data': [
'views/view_only_kiosk.xml'
    ],
    'qweb': [
        'static/src/xml/hr_attendance.xml'
             ],

}
