// Call the dataTables jQuery plugin
$(document).ready( function () {
  $('#dataTable').DataTable({
  dom: 'B<"clear">lfrtip',
  order: [[ 0, "desc" ]],
  buttons: {
      name: 'primary',
      buttons: [ 'copy' , 'csv','excel','pdf']
      }}
  );
} );