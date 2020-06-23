<template>
  <div class="home">
    <table>
      <tr v-for='course in courses' :key='course.cid'>
        <courserec :course='course' @updrec='updaterec' @delrec='deleterec'></courserec>
      </tr>
    </table>
    <button id='add' @click='addrec'>Add courses</button>
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
      alert(coursedat);
    },
    deleterec(coursedat) {
      alert(coursedat);
    },
    addrec() {
      alert('sdcf');
    },
    getCourse() {
      const path = 'http://localhost:5000/courses/check_course_json';
      console.log(path);
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
  updated() {
    this.getCourse();
  },
};
</script>
