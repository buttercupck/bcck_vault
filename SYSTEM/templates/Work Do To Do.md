---
date: <% tp.date.now("YYYY-MM-DD") %>
type: daily-log
aliases:
  - <% tp.date.now("MMMDD") %>
tags:
  - daily-log
---

## First thing:
---

## Immediate Tasks (Today)

### INTERCOM
- [ ] 

---

## Eventual Tasks

<%*
// Get previous day's date
const previousDay = tp.date.now("YYYY-MM-DD", -1);
const previousDayFile = `DAILY-LOGS/${previousDay}.md`;

// Try to read previous day's file
try {
    const previousContent = await tp.file.find_tfile(previousDayFile);
    if (previousContent) {
        const fileContent = await app.vault.read(previousContent);
        
        // Enhanced regex to handle various separators
        const eventualTasksRegex = /## Eventual (?:Tasks|To-Do)\s*([\s\S]*?)(?=\s*---|\s*##|$)/;
        const match = fileContent.match(eventualTasksRegex);
        
        if (match) {
            const eventualTasksSection = match[1].trim();
            
            if (eventualTasksSection) {
                // Find unchecked tasks (- [ ])
                const lines = eventualTasksSection.split('\n');
                let currentSilo = null;
                let tasksBySilo = {};
                let hasUncompletedTasks = false;
                
                lines.forEach(line => {
                    const trimmedLine = line.trim();
                    if (trimmedLine.startsWith('### ')) {
                        currentSilo = trimmedLine;
                        if (!tasksBySilo[currentSilo]) {
                            tasksBySilo[currentSilo] = [];
                        }
                    } else if (trimmedLine.match(/^- \[ \]/)) {
                        hasUncompletedTasks = true;
                        if (currentSilo) {
                            tasksBySilo[currentSilo].push(trimmedLine);
                        }
                    }
                });
                
                if (hasUncompletedTasks) {
                    // Output tasks by silo
                    for (const [silo, tasks] of Object.entries(tasksBySilo)) {
                        if (tasks.length > 0) {
                            tR += `${silo}\n`;
                            tasks.forEach(task => {
                                tR += `${task}\n`;
                            });
                            tR += '\n';
                        }
                    }
                    
                    // Add INTERCOM if not found
                    if (!Object.keys(tasksBySilo).some(silo => silo.includes('INTERCOM') || silo.includes('Intercom'))) {
                        tR += "### INTERCOM\n- [ ] \n\n";
                    }
                    
                    // Add placeholder
                    tR += "### [Silo Placeholder]\n- [ ] \n";
                } else {
                    tR += "### INTERCOM\n- [ ] \n\n### [Silo Placeholder]\n- [ ] \n";
                }
            } else {
                tR += "### INTERCOM\n- [ ] \n\n### [Silo Placeholder]\n- [ ] \n";
            }
        } else {
            tR += "### INTERCOM\n- [ ] \n\n### [Silo Placeholder]\n- [ ] \n";
        }
    } else {
        tR += "### INTERCOM\n- [ ] \n\n### [Silo Placeholder]\n- [ ] \n";
    }
} catch (error) {
    tR += `### INTERCOM\n- [ ] Debug: ${error.message}\n\n### [Silo Placeholder]\n- [ ] \n`;
}
%>

---

## Completed Tasks

### INTERCOM
- [ ] 

---

## Notes & Reflections

---

## Progressions

---

## Decisions
