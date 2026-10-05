# ruff: noqa: E402
import importlib
import sys

__version__ = "1.0.0"
__variant__ = "catalog"


class _ExtensionAliasFinder:
    """Redirects all 'openg2p_registry_extensions.*' imports to 'openg2p_registry_catalog_extension.*'
    without re-executing modules or duplicating SQLAlchemy table metadata.
    """

    def find_spec(self, fullname, path, target=None):
        if fullname == "openg2p_registry_extensions" or fullname.startswith("openg2p_registry_extensions."):
            real_name = fullname.replace("openg2p_registry_extensions", "openg2p_registry_catalog_extension", 1)
            if real_name in sys.modules:
                mod = sys.modules[real_name]
                sys.modules[fullname] = mod
                return mod.__spec__
            try:
                mod = importlib.import_module(real_name)
                sys.modules[fullname] = mod
                return mod.__spec__
            except Exception:
                return None
        return None


if not any(isinstance(f, _ExtensionAliasFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, _ExtensionAliasFinder())

# Pre-populate primary extension submodules into sys.modules
for _sub in (
    "",
    ".config",
    ".app",
    ".register_domain",
    ".register_domain.models",
    ".register_domain.schemas",
    ".register_domain.services",
    ".register_domain.factory",
):
    try:
        _m = importlib.import_module(f"openg2p_registry_catalog_extension{_sub}")
        sys.modules[f"openg2p_registry_extensions{_sub}"] = _m
    except Exception:
        pass
