<template>
  <div id="courseadd-form">
    <b-form @submit.prevent="handle">
    <label>Course ID</label>
    <b-input :state='cidstate' placeholder = "Enter CID"
    v-model = 'course.id'  required >
    </b-input>
    <br>

    <label>Course name</label>
    <b-input :state='cnstate' placeholder = "Enter course name"
    v-model = 'course.name' required ></b-input>
    <br>

    <b-button type="submit"> Add Course </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'AddCourseform',
  data() {
    return {
      course: {
        id: '', name: '',
      },
    };
  },
  computed: {
    cidstate() {
      return this.course.id.length > 0;
    },
    cnstate() {
      return this.course.name.length > 0;
    },
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
