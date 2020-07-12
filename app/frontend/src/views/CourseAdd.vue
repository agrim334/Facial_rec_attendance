<template>
  <div class="home">
    <AddCourseForm @courseadd="add">
    </AddCourseForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import AddCourseForm from '@/components/AddCourse.vue';

export default {
  name: 'AddCourse',
  components: {
    AddCourseForm,
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    add(data) {
      const path = 'courses/add_course_json';
      const updat = data;
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then((response) => {
          alert(response.data.result);
        })
        .catch((error) => {
          alert(error.response.data.result);
          console.error(error);
        });
    },
  },
  created() {
    if (!this.$store.getters.isAuthenticated) {
      alert("Session expired. You have to login again");
      this.logout();
    }
  },
};
</script>
