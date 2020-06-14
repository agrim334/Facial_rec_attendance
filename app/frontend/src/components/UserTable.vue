<template>
 <div>
  <table>
    <tbody>
      <tr v-for='user in users' :key='user.id'>
        <td>{{ user.id }}</td>
        <td>{{ user.username }}</td>
        <td>{{ user.email }}</td>
        <td>{{ user.dept }}</td>
        <td>{{ user.role }}</td>
      </tr>
    </tbody>
  </table>
 </div>
</template>

<script>
export default {
  name: 'UserTable',
  data() {
    return { user: Array };
  },
};
</script>
