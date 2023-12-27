controller_template = """
package {parentPackageName}.{packageName};

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("{packageName}s")
@RequiredArgsConstructor
public class {capitalizedPackageName}Controller {
    private final {capitalizedPackageName}Service {packageName}Service;
}
"""
