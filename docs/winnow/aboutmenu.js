// This manages the menu system
$(function() {
	
	$('.tab-panels .tabs li').on('click', function() {
		// Get the particular tab-panel the 'tab' is part of
		var panel = $(this).closest('.tab-panels');
		
		// The current 'active' tab (this can be null)
		var activeTab = panel.find('.tabs li.active');
		
		// The current 'active' panel (this can be null)
		var activePanel = panel.find('.panel.active');
		
		// The selected tab (this can NOT be null)
		var selectedTab = $(this);
		
		// The associated selected panel (this can NOT be null)
		var panelToShowRel = $(this).attr('rel');
		var panelToShow = $('#'+panelToShowRel);

		// The 'active' tab should go inactive (no matter what)
		if (activeTab.length) {
			activeTab.removeClass('active');
		} else {
			// no tab to remove 'active' from
		}
		
		// If the selected tab is not the active tab, then make it active
		if (!(selectedTab.is(activeTab))) {
			selectedTab.addClass('active');
		} else {
			// the active tab was clicked on, so no other
			// active tab to highlight
		}
		
		// If the active tab was selected, no panels should be open
		if (selectedTab.is(activeTab)) {
			// If the active panel exists, close it
			if (activePanel.length) {
				activePanel.removeClass('active');
			} else {
				// there is no active panel to hide
				// (leave this here to help understanding the logic)
			}
		} else {
			if (activePanel.length) {
				// A panel is already open, so close it, then open the new one.
				activePanel.removeClass('active');
				panelToShow.addClass('active');
			} else {
				// No panel is open, so just open the new one
				panelToShow.addClass('active');
			}
		}
	});

});
