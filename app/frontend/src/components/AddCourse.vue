<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>Course ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'course.id' />
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
        id: '', name: '',
      },
    };
  },
  methods: {
    handle() {
      let f = 0;
      if (this.course.id === null || this.course.id === '') {
        alert('fill course id');
        f = 1;
      }
      if (this.course.name === null || this.course.name === '') {
        alert('fill course name');
        f = 1;
      }
      if (f === 0) {
        this.$emit('courseadd', this.course);
      }
    },
  },
};
</script>
