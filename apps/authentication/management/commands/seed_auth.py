"""
Management command to seed authentication data
Creates default roles, resource groups, and permissions
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.authentication.models import Role, Permission, ResourceGroup, RolePermission


class Command(BaseCommand):
    help = 'Seed authentication data with default roles and permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing data before seeding',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Clearing existing data...')
            RolePermission.objects.all().delete()
            Permission.objects.all().delete()
            ResourceGroup.objects.all().delete()
            Role.objects.all().delete()
            self.stdout.write(self.style.WARNING('Existing data cleared'))

        # Create Resource Groups
        self.stdout.write('Creating resource groups...')
        resource_groups = self.create_resource_groups()
        self.stdout.write(self.style.SUCCESS(f'Created {len(resource_groups)} resource groups'))

        # Create Permissions
        self.stdout.write('Creating permissions...')
        permissions = self.create_permissions(resource_groups)
        self.stdout.write(self.style.SUCCESS(f'Created {len(permissions)} permissions'))

        # Create Roles
        self.stdout.write('Creating roles...')
        roles = self.create_roles()
        self.stdout.write(self.style.SUCCESS(f'Created {len(roles)} roles'))

        # Assign Permissions to Roles
        self.stdout.write('Assigning permissions to roles...')
        self.assign_permissions(roles, permissions)
        self.stdout.write(self.style.SUCCESS('Permissions assigned to roles'))

        self.stdout.write(self.style.SUCCESS('\n✅ Authentication data seeded successfully!'))
        self.print_summary(roles, resource_groups, permissions)

    def create_resource_groups(self):
        """Create resource groups for different modules"""
        groups_data = [
            # Authentication & Users
            {'name': 'users', 'module': 'authentication', 'description': 'User management'},
            {'name': 'roles', 'module': 'authentication', 'description': 'Role management'},
            {'name': 'permissions', 'module': 'authentication', 'description': 'Permission management'},
            {'name': 'audit', 'module': 'authentication', 'description': 'Audit logs'},
            
            # Students
            {'name': 'students.records', 'module': 'students', 'description': 'Student records'},
            {'name': 'students.enrollment', 'module': 'students', 'description': 'Student enrollment'},
            
            # Admissions
            {'name': 'admissions.applications', 'module': 'admissions', 'description': 'Application management'},
            {'name': 'admissions.merit_lists', 'module': 'admissions', 'description': 'Merit list generation'},
            
            # Courses
            {'name': 'courses.content', 'module': 'courses', 'description': 'Course content management'},
            {'name': 'courses.assignments', 'module': 'courses', 'description': 'Assignment management'},
            {'name': 'courses.grades', 'module': 'courses', 'description': 'Grade management'},
            
            # Finance
            {'name': 'finance.fees', 'module': 'finance', 'description': 'Fee structure management'},
            {'name': 'finance.payments', 'module': 'finance', 'description': 'Payment processing'},
            {'name': 'finance.invoices', 'module': 'finance', 'description': 'Invoice management'},
            
            # Library
            {'name': 'library.books', 'module': 'library', 'description': 'Book management'},
            {'name': 'library.circulation', 'module': 'library', 'description': 'Book circulation'},
            
            # HR & Faculty
            {'name': 'hr.employees', 'module': 'hr', 'description': 'Employee management'},
            {'name': 'hr.attendance', 'module': 'hr', 'description': 'Attendance tracking'},
            {'name': 'hr.payroll', 'module': 'hr', 'description': 'Payroll management'},
            
            # Analytics
            {'name': 'analytics.reports', 'module': 'analytics', 'description': 'Report generation'},
            {'name': 'analytics.dashboards', 'module': 'analytics', 'description': 'Dashboard access'},
        ]

        groups = {}
        for data in groups_data:
            group, created = ResourceGroup.objects.get_or_create(
                name=data['name'],
                defaults={
                    'module': data['module'],
                    'description': data['description']
                }
            )
            groups[data['name']] = group
            if created:
                self.stdout.write(f'  ✓ Created resource group: {data["name"]}')

        return groups

    def create_permissions(self, resource_groups):
        """Create permissions for each resource group"""
        actions = ['view', 'create', 'update', 'delete', 'approve', 'export']
        permissions = {}

        for group_name, group in resource_groups.items():
            # Not all actions apply to all resources
            applicable_actions = actions.copy()
            
            # Audit logs are read-only
            if 'audit' in group_name:
                applicable_actions = ['view', 'export']
            # Dashboards and reports
            elif 'dashboard' in group_name or 'report' in group_name:
                applicable_actions = ['view', 'export']
            
            for action in applicable_actions:
                perm, created = Permission.objects.get_or_create(
                    resource_group=group,
                    action=action,
                    defaults={'description': f'{action.title()} {group_name}'}
                )
                permissions[f'{group_name}:{action}'] = perm

        return permissions

    def create_roles(self):
        """Create default roles"""
        roles_data = [
            {
                'name': 'Super Admin',
                'description': 'Full system access with all permissions'
            },
            {
                'name': 'Admin',
                'description': 'Administrative access to most features'
            },
            {
                'name': 'Management',
                'description': 'Management level access to reports and oversight'
            },
            {
                'name': 'Faculty',
                'description': 'Faculty access to courses, grades, and students'
            },
            {
                'name': 'Staff',
                'description': 'Staff access to operational features'
            },
            {
                'name': 'Student',
                'description': 'Student access to own records and courses'
            },
            {
                'name': 'Parent',
                'description': 'Parent access to child records'
            },
            {
                'name': 'Admissions Officer',
                'description': 'Access to admissions and application management'
            },
            {
                'name': 'Finance Officer',
                'description': 'Access to finance and payment management'
            },
            {
                'name': 'Librarian',
                'description': 'Access to library management'
            },
        ]

        roles = {}
        for data in roles_data:
            role, created = Role.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'is_active': True
                }
            )
            roles[data['name']] = role
            if created:
                self.stdout.write(f'  ✓ Created role: {data["name"]}')

        return roles

    def assign_permissions(self, roles, permissions):
        """Assign permissions to roles based on role type"""
        
        # Super Admin gets all permissions
        super_admin = roles['Super Admin']
        for perm in Permission.objects.all():
            RolePermission.objects.get_or_create(role=super_admin, permission=perm)

        # Admin gets most permissions except sensitive HR and finance
        admin = roles['Admin']
        admin_perms = [p for p in permissions.keys() 
                      if not any(x in p for x in ['payroll', 'hr.employees:delete'])]
        for perm_key in admin_perms:
            RolePermission.objects.get_or_create(role=admin, permission=permissions[perm_key])

        # Management gets view and export permissions
        management = roles['Management']
        management_perms = [p for p in permissions.keys() if ':view' in p or ':export' in p]
        for perm_key in management_perms:
            RolePermission.objects.get_or_create(role=management, permission=permissions[perm_key])

        # Faculty gets course and student-related permissions
        faculty = roles['Faculty']
        faculty_perms = [p for p in permissions.keys() 
                        if any(x in p for x in ['courses', 'students.records:view', 'grades'])]
        for perm_key in faculty_perms:
            RolePermission.objects.get_or_create(role=faculty, permission=permissions[perm_key])

        # Admissions Officer
        admissions = roles['Admissions Officer']
        admissions_perms = [p for p in permissions.keys() if 'admissions' in p or 'students.enrollment' in p]
        for perm_key in admissions_perms:
            RolePermission.objects.get_or_create(role=admissions, permission=permissions[perm_key])

        # Finance Officer
        finance = roles['Finance Officer']
        finance_perms = [p for p in permissions.keys() if 'finance' in p]
        for perm_key in finance_perms:
            RolePermission.objects.get_or_create(role=finance, permission=permissions[perm_key])

        # Librarian
        librarian = roles['Librarian']
        librarian_perms = [p for p in permissions.keys() if 'library' in p]
        for perm_key in librarian_perms:
            RolePermission.objects.get_or_create(role=librarian, permission=permissions[perm_key])

        # Staff gets basic operational permissions
        staff = roles['Staff']
        staff_perms = [p for p in permissions.keys() 
                      if ':view' in p and any(x in p for x in ['students', 'courses', 'library'])]
        for perm_key in staff_perms:
            RolePermission.objects.get_or_create(role=staff, permission=permissions[perm_key])

    def print_summary(self, roles, resource_groups, permissions):
        """Print summary of seeded data"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('SEEDING SUMMARY'))
        self.stdout.write('='*60)
        
        self.stdout.write(f'\nResource Groups: {len(resource_groups)}')
        for name in sorted(resource_groups.keys()):
            self.stdout.write(f'  • {name}')
        
        self.stdout.write(f'\nRoles: {len(roles)}')
        for name, role in roles.items():
            perm_count = RolePermission.objects.filter(role=role).count()
            self.stdout.write(f'  • {name}: {perm_count} permissions')
        
        self.stdout.write(f'\nTotal Permissions: {len(permissions)}')
        self.stdout.write('='*60 + '\n')
