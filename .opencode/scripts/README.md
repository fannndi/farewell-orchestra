# Automation Scripts

Scripts for project management and automation.

## Available Scripts

### Project Management
| Script | Purpose | Usage |
|--------|---------|-------|
| `verify-docs.ps1` | Check docs completeness | `.\verify-docs.ps1 -ProjectPath "C:\path"` |
| `project-health.ps1` | Project health score | `.\project-health.ps1 -ProjectPath "C:\path"` |
| `project-dashboard.ps1` | Project overview | `.\project-dashboard.ps1 -ProjectPath "C:\path"` |
| `generate-sub-project.ps1` | Generate sub-project.md | `.\generate-sub-project.ps1 -ProjectPath "C:\path"` |

### Project Type
| Script | Purpose | Usage |
|--------|---------|-------|
| `detect-project-type.ps1` | Detect project type | `.\detect-project-type.ps1 -ProjectPath "C:\path"` |

### Dependencies & Testing
| Script | Purpose | Usage |
|--------|---------|-------|
| `auto-deps.ps1` | Auto-install dependencies | `.\auto-deps.ps1 -ProjectPath "C:\path"` |
| `auto-test.ps1` | Auto-run tests | `.\auto-test.ps1 -ProjectPath "C:\path"` |

## Usage Examples

### Full Project Setup
```powershell
# 1. Detect project type
.\detect-project-type.ps1 -ProjectPath "C:\Users\me\my-app"

# 2. Install dependencies
.\auto-deps.ps1 -ProjectPath "C:\Users\me\my-app"

# 3. Check docs
.\verify-docs.ps1 -ProjectPath "C:\Users\me\my-app"

# 4. Run tests
.\auto-test.ps1 -ProjectPath "C:\Users\me\my-app"

# 5. View dashboard
.\project-dashboard.ps1 -ProjectPath "C:\Users\me\my-app"
```

### Health Check
```powershell
.\project-health.ps1 -ProjectPath "C:\Users\me\my-app"
```

### Generate Documentation
```powershell
.\generate-sub-project.ps1 -ProjectPath "C:\Users\me\my-app" -ProjectName "My App"
```

## Adding New Scripts

To add a new script:
1. Create `.ps1` file in this directory
2. Add usage comment at top
3. Update this README
4. Test with sample project
