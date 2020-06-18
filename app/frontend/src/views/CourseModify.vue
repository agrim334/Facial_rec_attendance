<template>
  <div class="home">
    <ModifyCourseForm :courserec = 'course' @courseupd='updaterec'> </ModifyCourseForm>
  </div>

</template>

<script>
// @ is an alias to /src
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
      alert(modcourse);
    },
  },
};
</script>
