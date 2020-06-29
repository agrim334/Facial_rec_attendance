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
      const path = 'http://localhost:5000/courses/modify_course_json';
      const updat = { old: this.course, new: modcourse };
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then(() => {
          console.log(this);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
