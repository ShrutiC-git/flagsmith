from environments.permissions.constants import (
    APPROVE_CHANGE_REQUEST,
    CREATE_CHANGE_REQUEST,
    UPDATE_FEATURE_STATE,
)


def test_add_change_request_permissions_adds_correct_permissions_if_user_has_update_fs(
    environment, django_user_model, migrator
):
    # Given
    old_state = migrator.apply_initial_migration(
        ("environment_permissions", "0003_add_manage_identities_permission")
    )
    user_model = old_state.apps.get_model("users", "FFAdminUser")
    user_environment_permission_model = old_state.apps.get_model(
        "environment_permissions", "UserEnvironmentPermission"
    )
    permission_model = old_state.apps.get_model("permissions", "PermissionModel")
    organisation_model = old_state.apps.get_model("organisations", "Organisation")
    project_model = old_state.apps.get_model("projects", "Project")
    environment_model = old_state.apps.get_model("environments", "Environment")

    org = organisation_model.objects.create(name="test org")
    project = project_model.objects.create(name="test project", organisation=org)
    environment = environment_model.objects.create(name="test env", project=project)

    # a user with UPDATE_FEATURE_STATE permission
    user = user_model.objects.create(email="test@example.com")
    user_environment_permission = user_environment_permission_model.objects.create(
        user=user, environment=environment
    )
    update_feature_state_permission = permission_model.objects.get(
        key=UPDATE_FEATURE_STATE
    )
    user_environment_permission.permissions.add(update_feature_state_permission)

    # When
    new_state = migrator.apply_tested_migration(
        ("environment_permissions", "0004_add_change_request_permissions")
    )

    # Then
    new_user_environment_permission_model = new_state.apps.get_model(
        "environment_permissions", "UserEnvironmentPermission"
    )

    new_user_environment_permission = new_user_environment_permission_model.objects.get(
        id=user_environment_permission.id
    )
    assert new_user_environment_permission.permissions.count() == 3
    assert list(
        new_user_environment_permission.permissions.order_by("key").values_list(
            flat=True
        )
    ) == [APPROVE_CHANGE_REQUEST, CREATE_CHANGE_REQUEST, UPDATE_FEATURE_STATE]


def test_add_change_request_permissions_does_nothing_if_user_does_not_have_update_fs(
    environment, django_user_model, migrator
):
    # Given
    old_state = migrator.apply_initial_migration(
        ("environment_permissions", "0003_add_manage_identities_permission")
    )
    user_model = old_state.apps.get_model("users", "FFAdminUser")
    organisation_model = old_state.apps.get_model("organisations", "Organisation")
    project_model = old_state.apps.get_model("projects", "Project")
    environment_model = old_state.apps.get_model("environments", "Environment")

    org = organisation_model.objects.create(name="test org")
    project = project_model.objects.create(name="test project", organisation=org)
    environment = environment_model.objects.create(name="test env", project=project)

    # a user without UPDATE_FEATURE_STATE permission
    user = user_model.objects.create(email="test@example.com")

    # When
    new_state = migrator.apply_tested_migration(
        ("environment_permissions", "0004_add_change_request_permissions")
    )

    # Then
    assert (
        not new_state.apps.get_model(
            "environment_permissions", "UserEnvironmentPermission"
        )
        .objects.filter(user_id=user.id, environment_id=environment.id)
        .exists()
    )
