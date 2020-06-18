<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>Course ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'course.cid' />
    <br>

    <label>Course name</label>
    <input type="text" placeholder = "Enter course name" v-model = 'course.name' />
    <br>

    <input type="submit" value="Add Course" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'AddCourseForm',
  data() {
    return {
      course: {
        cid: '', name: '',
      },
    };
  },
  methods: {
    handle() {
      this.$emit('courseadd', this.course);
    },
  },
};
</script>
