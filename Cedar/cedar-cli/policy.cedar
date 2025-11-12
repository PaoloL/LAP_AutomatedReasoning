// Allow Viewers to getBike and allow only Admins to updateBike

// Grant read access to members of the "Viewers" group
permit (
    principal in Recube::MyApp::Roles::"Viewer",
    action in [Recube::MyApp::Action::"getBike", Recube::MyApp::Action::"getCars"],
    resource
);

// Grant all access to members of the "Admins" group
permit (
    principal in Recube::MyApp::Roles::"Admin",
    action,
    resource
);