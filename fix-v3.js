// Shared kiosk navigation repair.
(function(){
  const originalAdminLogin = window.adminLogin;

  window.showAdminTab = function(tab){
    const sections = {
      dashboard: 'adminDashboard',
      staff: 'adminStaff',
      reports: 'adminReports',
      backup: 'adminBackup'
    };
    const buttons = {
      dashboard: 'adminDashTab',
      staff: 'adminStaffTab',
      reports: 'adminReportTab',
      backup: 'adminBackupTab'
    };

    Object.keys(sections).forEach(key => {
      const section = document.getElementById(sections[key]);
      const button = document.getElementById(buttons[key]);
      if (section) section.classList.toggle('hidden', key !== tab);
      if (button) button.classList.toggle('active', key === tab);
    });

    if (tab === 'dashboard' && typeof renderAdmin === 'function') renderAdmin();
    if (tab === 'staff' && typeof renderStaff === 'function') renderStaff();
    if (tab === 'reports' && typeof setupReports === 'function') setupReports();
  };

  window.openEmployeeRegistration = function(){
    sessionStorage.setItem('sak_open_staff_after_login', '1');
    if (typeof openAdminLogin === 'function') openAdminLogin();
  };

  if (typeof originalAdminLogin === 'function') {
    window.adminLogin = async function(){
      await originalAdminLogin();
      if (!document.getElementById('adminView').classList.contains('hidden')) {
        if (sessionStorage.getItem('sak_open_staff_after_login') === '1') {
          sessionStorage.removeItem('sak_open_staff_after_login');
          window.showAdminTab('staff');
        }
      }
    };
  }
})();
