<template>
  <div class="home">
    <b-table :items='courses'>
      <template v-slot:cell(actions)='row'>
        <b-button @click='deleterec(row)'> Delete </b-button>
        <b-button @click='updaterec(row)'> Update </b-button>
      </template>
    </b-table>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'CourseTable',
  props: {
    courses: Array,
  },
  methods: {
    updaterec(coursedat) {
      this.$router.push({ name: 'CourseModify', params: { course: coursedat.item } });
    },
    deleterec(coursedat) {
      const path = 'http://localhost:5000/courses/delete_course_json';
      axios.post(path, coursedat.item.id)
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
