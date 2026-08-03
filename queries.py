def get_project_by_id(project_id):
    """Retrieves a project event by ID. Returns Project or None."""
    if isinstance(project_id, int):
        return db.session.get(Project, project_id)
    else:
        raise ValueError("Invalid Id!")


def create_project(project_data):
    """Creates a new project event. Returns new project"""
    ProjectEvt = Project(
        name=project_data.get("name"),
        notes=project_data.get("notes"),
        start_date=project_data.get("start_date"),
        end_date=project_data.get("end_date"),
        project_link=project_data.get("project_link"),
        hobby_id=project_data.get("hobby_id"),
        user_id=project_data.get("user_id"),
    )
    db.session.add(ProjectEvt)
    db.session.commit()
    return ProjectEvt


def update_project(project, fields_to_update):
    """Updates a project event. Returns updated ProjectEvent."""
    for field, value in fields_to_update.items():
        if field in project.__table__.columns.keys():
            setattr(project, field, value)
        else:
            raise ValueError(f"Invalid field: {field}")
    db.session.commit()
    return project


def delete_project(project_id):
    """Deletes a selected project. Future Scope: add in delete a post or update."""
    project = db.session.get(Project, project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        return True
    return False