repository_template = """package {parentPackageName}.{packageName};

import org.springframework.data.jpa.repository.JpaRepository;

public interface {capitalizedPackageName}Repository extends JpaRepository<{capitalizedPackageName}, Long> {}
"""
