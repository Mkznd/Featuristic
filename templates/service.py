service_template = """package {parentPackageName}.{packageName};

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class {capitalizedPackageName}Service {
    private final {capitalizedPackageName}Repository {packageName}Repository;
}
"""
