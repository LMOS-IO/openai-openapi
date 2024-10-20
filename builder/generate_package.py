from pathlib import Path
from datamodel_code_generator import InputFileType, generate, OpenAPIScope
from datamodel_code_generator import DataModelType, PythonVersion
import json
import warnings

from ruamel.yaml import YAML
from ruamel.yaml.error import ReusedAnchorWarning

# fix errors from ruamel.yaml
warnings.simplefilter("ignore", ReusedAnchorWarning)

# convert the yaml into json
yaml = YAML(typ="safe", pure=True)

with open("openapi.yaml") as stream:
    data = yaml.load(stream)

openapi_json = json.dumps(data)

# create a path for the new package
release_pkg_dir = Path('openai_types/')
release_pkg_dir.mkdir(parents=True, exist_ok=True)

# create types
output = Path(release_pkg_dir / '__init__.py')
generate(
    input_=openapi_json,
    input_file_type=InputFileType.OpenAPI,
    output=output,
    output_model_type=DataModelType.PydanticV2BaseModel,
    target_python_version=PythonVersion.PY_312,
    apply_default_values_for_required_fields=False,
    use_field_description=True,
    use_schema_description=True,
    # reuse_model=True,
    # use_subclass_enum=True,
    # use_default_kwarg=True,
    # field_constraints=True,
    # enum_field_as_literal="all",
    # openapi_scopes=[OpenAPIScope.Parameters, OpenAPIScope.Paths, OpenAPIScope.Schemas, OpenAPIScope.Tags],
    strict_nullable=True # https://github.com/koxudaxi/datamodel-code-generator/issues/327
)