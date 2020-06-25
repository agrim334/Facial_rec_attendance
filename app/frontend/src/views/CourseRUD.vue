<template>
  <div class="home">
    <table>
      <tr v-for='course in courses' :key='course.cid'>
        <courserec :course='course' @updrec='updaterec' @delrec='deleterec'></courserec>
      </tr>
    </table>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import courserec from '@/components/RUDCourse.vue';

export default {
  name: 'CourseTable',
  props: {
    courses: Array,
  },
  components: {
    courserec,
  },
  methods: {
    updaterec(coursedat) {
      this.$router.push({ name: 'CourseModify', params: { course: coursedat } });
    },
    deleterec(coursedat) {
      const path = 'http://localhost:5000/courses/delete_course_json';
      axios.post(path, coursedat.id)
        .then(() => {
          this.getCourse();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getCourse() {
      const path = 'http://localhost:5000/courses/check_course_json';
      axios.get(path)
        .then((res) => {
          this.courses = res.data.records;
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
