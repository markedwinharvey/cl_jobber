$(document)
	.on('click','.state',function(){
		$(this).next().toggleClass('hidden');
		$(this).toggleClass('backlit');
	})
	
	.on('click','.sub_check',function(){
		var id = $(this).attr('id');
		if (this.checked){
			var name = $(this).attr('name');
			$('#selections').append(
				'<div class="selection" id="'+id+'_select" name="'+name+'"><button class="remove_selection">remove</button> '+name+'</div>'
			);
		}
		else{
			$('#'+id+'_select').remove();
		}
	})
	
	.on('click','#all',function(){
		all_check = this.checked;	
		$('.sub_check').each(function(){
			this.checked = all_check;	
		});
	})
	
	.on('click','.remove_selection',function(){
		var id = $(this).parent().attr('id').split('_select')[0];
		$('#'+id).prop('checked',false);
		$(this).parent().remove();
		
	})
	
	.on('click','#send_data',function(){
		var sel = []
		var selections = $('.selection').each(function(){
			sel.push($(this).attr('name'));
			//sel.push(($(this).attr('id').split('_select')[0]));	
		});
		if (sel.length > 0){
			$.ajax({
				method:'post',
				url:'cgi-bin/redirect.py',
				data:{
					'package':
						JSON.stringify({
							'file':'cgi-bin/fetch_pages.py',
							'contents':sel
						})
				
				
					//'file':'cgi-bin/fetch_pages.py',
					//'package':'some_shit'//JSON.stringify(sel)
				},
				success:function(result){
					print(result);
				}
			});
			
			/*
			$.ajax({
				method:'post',
				url:'cgi-bin/fetch_pages.py',
				data:{'package':JSON.stringify(sel)},
				success:function(result){
					print('Message received');
				}
			});
			*/
		}
	
	});
	