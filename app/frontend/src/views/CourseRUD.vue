<template>
  <div class="home">
  <CourseRec :courses='courses' @updrec='updaterec' @delrec='deleterec'>
  </CourseRec>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import CourseRec from '../components/RUDCourse.vue';

export default {
  name: 'CourseTable',
  props: {
    courses: Array,
  },
  components: {
    CourseRec,
  },
  methods: {
    updaterec(coursedat) {
      this.$router.push({ name: 'CourseModify', params: { course: coursedat } });
    },
    deleterec(coursedat) {
      const path = 'http://localhost:5000/courses/delete_course_json';
      this.$store.dispatch('authrequest', { url: path, data: coursedat.id })
        .then(() => {
          this.getCourse();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getCourse() {
      const path = 'http://localhost:5000/courses/check_course_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((res) => {
          this.courses = res.data.records;
          for (let i = 0; i < this.courses.length; i += 1) {
            this.courses[i].actions = '';
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getCourse();
  },
};
</script>
