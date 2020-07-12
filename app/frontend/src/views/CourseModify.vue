<template>
  <div class="home">
    <ModifyCourseForm :courserec = 'course' @courseupd='updaterec'> </ModifyCourseForm>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import ModifyCourseForm from '@/components/ModifyCourse.vue';

export default {
  name: 'CourseModify',
  props: {
    course: Array,
  },
  components: {
    ModifyCourseForm,
  },
  methods: {
    updaterec(modcourse) {
      const path = 'courses/modify_course_json';
      const updat = { old: this.course, new: modcourse };
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then((response) => {
          alert(response.data.result);
          console.log(response);
        })
        .catch((error) => {
          alert(error.response.data.result);
          console.error(error);
        });
    },
  },
};
</script>
