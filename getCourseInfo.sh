#!/bin/bash
endpoint=api.umd.io/v0/courses?course_id=$1
##dos2unix $endpoint
echo $endpoint
curl $endpoint > C:/Users/Nikhil/CourseEval/currentCourseInfo.txt
