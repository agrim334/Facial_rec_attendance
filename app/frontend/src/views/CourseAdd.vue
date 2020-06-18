<template>
  <div class="home">
    <AddCourseForm @courseadd="validate">
    </AddCourseForm>
  </div>
</template>

<script>
// @ is an alias to /src
import AddCourseForm from '@/components/AddCourse.vue';

export default {
  name: 'AddCourse',
  components: {
    AddCourseForm,
  },
  methods: {
    validate(newcourse) {
      if (newcourse.cid === null || newcourse.cid === '') {
        alert('Fill in user name');
      }
      if (newcourse.name === null || newcourse.name === '') {
        alert('Fill in first name');
      }
    },
  },
};
</script>
