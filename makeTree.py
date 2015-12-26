import json
import subprocess
import sys

def parseDescription(wordList):

    prereqList = [];

    if(len(wordList) != 0):
        startIndex = 0; ##not inclusive
        endIndex = 0;  ##inclusive

        startFound = False;
        endFound = False;
        for i in range(0,len(wordList) - 1):
            if(wordList[i] == 'Prerequisite:'):
                startIndex = i;
                startFound = True;

            word = wordList[i];
            if((word[len(word) - 1] == '.') and startFound):
                endIndex = i;
                endFound = True;

            if(startFound and endFound):
                break;

        for i in range(startIndex + 1, endIndex):
            word = wordList[i];

            if(len(word) != 0):
                while(not word[0].isalpha() and not word[0].isdigit()):
                    word = word.lstrip(word[0]);
                    if(len(word) == 0):
                        break;

            if(len(word) != 0):
                while(not word[len(word) - 1].isalpha() and
                      not word[len(word) - 1].isdigit()):
                    word = word.rstrip(word[len(word) - 1]);
                    if(len(word) ==0):
                        break;

            if(len(word) == 7 and
               word[len(word) - 1].isdigit() and
               word[len(word) - 2].isdigit() and
               word[len(word) - 3].isdigit()):
                prereqList.append(word);

    return prereqList;
    
    

def makeTree(listPath):
    courseFile = open(listPath, 'r');
    courseList = json.load(courseFile);
    courseFile.close();
    
    while(len(courseList) != 0):
    	currentCourse = courseList.pop();
	courseID = str(currentCourse['course_id']);

	script = ['./getCourseInfo.sh', courseID];
	subprocess.call(script);

	info = open('./currentCourseInfo.txt','r');
	courseInfo = json.load(info);
	info.close();

	courseInfo = courseInfo.pop();
        prereqs = str(courseInfo['relationships']['prereqs']);

        treeFile = open('./treeFile.txt', 'a');
        
        if(prereqs == 'None'):
            description = str(courseInfo['description']);
            wordList = description.split();
        
            prereqList = parseDescription(wordList);
            if(len(prereqList) != 0):
                treeFile.write(courseID + ': ');
                for prereq in prereqList:
                    treeFile.write(prereq + ' ');
                treeFile.write('\n');
                    
        else:
            treeFile.write(courseID + ': ' + prereqs + '\n');

            
	treeFile.close();

            

if(__name__ == '__main__'):
    makeTree(str(sys.argv[1]));
    
	
